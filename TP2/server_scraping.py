import argparse
import asyncio
import aiohttp.web
import datetime
from urllib.parse import urlparse
import socket

from common.protocol import Protocol
from scraper.html_parser import HTMLParser
from scraper.metadata_extractor import MetadataExtractor
from scraper.async_http import AsyncHTTPClient


# Configuracion del servidor de procesamiento
PROCESSING_SERVER_IP = '127.0.0.1'
PROCESSING_SERVER_PORT = 8001

# Semáforo para limitar conexiones concurrentes
connection_semaphore = None


def is_valid_url(url):
    """Valida que la URL tenga formato correcto"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
    except:
        return False


async def connect_to_processing_server(max_retries=3):
    """Establece una conexion asincrona al servidor de procesamiento con reintentos."""
    for attempt in range(max_retries):
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(PROCESSING_SERVER_IP, PROCESSING_SERVER_PORT),
                timeout=5.0
            )
            return reader, writer
        except asyncio.TimeoutError:
            print(f"Timeout al conectar con el servidor de procesamiento (intento {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
        except ConnectionRefusedError:
            print(f"Conexión rechazada por el servidor de procesamiento (intento {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Error al conectar con el servidor de procesamiento (intento {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
    return None, None


async def handle_scrape(request):
    """Handler para la ruta /scrape"""
    global connection_semaphore
    
    url = request.query.get('url')
    if not url:
        return aiohttp.web.json_response(
            {'status': 'error', 'message': 'Parámetro URL no especificado'}, 
            status=400
        )
    
    # Validar formato de URL
    if not is_valid_url(url):
        return aiohttp.web.json_response(
            {'status': 'error', 'message': 'Formato de URL inválido'}, 
            status=400
        )

    print(f"Solicitud de scraping recibida para URL: {url}")

    # Usar semáforo para limitar conexiones concurrentes
    async with connection_semaphore:
        # Usar context manager para el cliente HTTP
        async with AsyncHTTPClient(timeout=30) as http_client:
            scraping_data = {}
            processing_data = {}
            status = 'success'
            error_message = None

            try:
                # Realizar scraping HTML
                html_content = await http_client.fetch(url)
                soup = HTMLParser.parse_html(html_content)

                scraping_data = {
                    'title': HTMLParser.extract_title(soup),
                    'links': HTMLParser.extract_links(soup, url),
                    'meta_tags': MetadataExtractor.extract_all_metadata(soup),
                    'structure': HTMLParser.extract_structure(soup),
                    'images_count': HTMLParser.count_images(soup)
                }

                # Comunicar con servidor de procesamiento (con reintentos)
                reader, writer = await connect_to_processing_server()
                if reader and writer:
                    try:
                        processing_request = {'url': url}
                        await Protocol.send_async(writer, processing_request)
                        
                        # Esperar respuesta con timeout
                        processing_response = await asyncio.wait_for(
                            Protocol.receive_async(reader),
                            timeout=90.0  # Timeout generoso para procesamiento
                        )

                        if processing_response.get('status') == 'success':
                            processing_data = processing_response.get('processing_data', {})
                        else:
                            status = 'warning'
                            error_message = f"Error del servidor de procesamiento: {processing_response.get('message', 'Error desconocido')}"
                            print(error_message)
                    except asyncio.TimeoutError:
                        status = 'warning'
                        error_message = "Timeout esperando respuesta del servidor de procesamiento"
                        print(error_message)
                    except Exception as e:
                        status = 'warning'
                        error_message = f"Error comunicando con servidor de procesamiento: {str(e)}"
                        print(error_message)
                    finally:
                        writer.close()
                        await writer.wait_closed()
                else:
                    status = 'warning'
                    error_message = "No se pudo conectar al servidor de procesamiento después de reintentos."
                    print(error_message)

            except asyncio.TimeoutError:
                status = 'error'
                error_message = "Timeout en scraping (30 segundos excedidos)."
                print(f"Scraping timeout para URL: {url}")
            except aiohttp.ClientError as e:
                status = 'error'
                error_message = f"Error de cliente HTTP: {str(e)}"
                print(f"Error de cliente al hacer scraping de URL {url}: {e}")
            except Exception as e:
                status = 'error'
                error_message = f"Error inesperado: {str(e)}"
                print(f"Error al hacer scraping de URL {url}: {e}")

        response_payload = {
            "url": url,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "scraping_data": scraping_data,
            "processing_data": processing_data,
            "status": status
        }
        if error_message:
            response_payload['error'] = error_message

        return aiohttp.web.json_response(response_payload)


def detect_ip_version(ip_address):
    """Detecta si una dirección IP es IPv4 o IPv6"""
    try:
        socket.inet_pton(socket.AF_INET, ip_address)
        return socket.AF_INET
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, ip_address)
            return socket.AF_INET6
        except socket.error:
            raise ValueError(f"Dirección IP inválida: {ip_address}")


async def start_server(ip, port, app):
    """Inicia el servidor con soporte dual-stack IPv4/IPv6"""
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    
    try:
        # Detectar versión de IP
        ip_version = detect_ip_version(ip)
        
        # Configurar el sitio TCP
        if ip_version == socket.AF_INET6:
            # Para IPv6, crear socket manualmente para configurar opciones
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Permitir dual-stack si la dirección es "::"
            if ip == "::":
                sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            
            sock.bind((ip, port))
            site = aiohttp.web.SockSite(runner, sock)
        else:
            # IPv4 normal
            site = aiohttp.web.TCPSite(runner, ip, port)
        
        await site.start()
        return runner, site
    except Exception as e:
        await runner.cleanup()
        raise e


async def main():
    global PROCESSING_SERVER_IP, PROCESSING_SERVER_PORT, connection_semaphore
    
    parser = argparse.ArgumentParser(description="Servidor de Scraping Web Asíncrono")
    parser.add_argument('-i', '--ip', type=str, required=True, 
                        help="Dirección de escucha (soporta IPv4/IPv6)")
    parser.add_argument('-p', '--port', type=int, required=True, 
                        help="Puerto de escucha")
    parser.add_argument('-w', '--workers', type=int, default=4, 
                        help="Número de workers/conexiones concurrentes (default: 4)")
    parser.add_argument('--processing_ip', type=str, default=PROCESSING_SERVER_IP,
                        help=f"IP del servidor de procesamiento (default: {PROCESSING_SERVER_IP})")
    parser.add_argument('--processing_port', type=int, default=PROCESSING_SERVER_PORT,
                        help=f"Puerto del servidor de procesamiento (default: {PROCESSING_SERVER_PORT})")

    args = parser.parse_args()

    # Configurar variables globales
    PROCESSING_SERVER_IP = args.processing_ip
    PROCESSING_SERVER_PORT = args.processing_port
    connection_semaphore = asyncio.Semaphore(args.workers)

    # Crear aplicación
    app = aiohttp.web.Application()
    app.router.add_get('/scrape', handle_scrape)

    print(f"Servidor de Scraping iniciando en {args.ip}:{args.port}")
    print(f"Conectando al servidor de procesamiento: {PROCESSING_SERVER_IP}:{PROCESSING_SERVER_PORT}")
    print(f"Conexiones concurrentes máximas: {args.workers}")
    
    try:
        runner, site = await start_server(args.ip, args.port, app)
        
        print("Servidor iniciado correctamente. Presiona Ctrl+C para detener.")
        
        # Mantener el servidor corriendo hasta que se interrumpa
        await asyncio.Event().wait()
    except ValueError as e:
        print(f"Error: {e}")
        return
    except OSError as e:
        print(f"Error al iniciar el servidor: {e}")
        return
    except KeyboardInterrupt:
        print("\n -- Servidor de Scraping detenido por el usuario. --")
    finally:
        if 'runner' in locals():
            await runner.cleanup()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n -- Terminando servidor... --")
