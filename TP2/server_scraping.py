import argparse
import asyncio
import aiohttp.web
import datetime
import socket
from urllib.parse import urlparse

from common.protocol import Protocol
from scraper.html_parser import HTMLParser
from scraper.metadata_extractor import MetadataExtractor
from scraper.async_http import AsyncHTTPClient


# Configuracion del servidor de procesamiento
PROCESSING_SERVER_IP = '127.0.0.1'
PROCESSING_SERVER_PORT = 8001


def is_valid_url(url):
    """Valida que la URL tenga formato correcto"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
    except:
        return False


def get_address_family(ip):
    """Detecta si la IP es IPv4 o IPv6"""
    try:
        socket.inet_pton(socket.AF_INET6, ip)
        return socket.AF_INET6
    except:
        return socket.AF_INET


async def connect_to_processing_server(max_retries=3):
    """Establece una conexion asincrona al servidor de procesamiento con reintentos."""
    for attempt in range(max_retries):
        try:
            reader, writer = await asyncio.open_connection(
                PROCESSING_SERVER_IP, 
                PROCESSING_SERVER_PORT
            )
            return reader, writer
        except Exception as e:
            print(f"Error al conectar con el servidor de procesamiento (intento {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(1)  # Esperar 1 segundo antes de reintentar
    return None, None


async def handle_scrape(request):
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

    # Usar context manager para el cliente HTTP
    async with AsyncHTTPClient(timeout=30) as http_client:
        scraping_data = {}
        processing_data = {}
        status = 'success'
        error_message = None

        try:
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
                    processing_response = await Protocol.receive_async(reader)

                    if processing_response.get('status') == 'success':
                        processing_data = processing_response.get('processing_data', {})
                    else:
                        status = 'warning'
                        error_message = f"Error del servidor de procesamiento: {processing_response.get('message', 'Error desconocido')}"
                        print(error_message)
                finally:
                    writer.close()
                    await writer.wait_closed()
            else:
                status = 'warning'
                error_message = "No se pudo conectar al servidor de procesamiento despues de reintentos."
                print(error_message)

        except asyncio.TimeoutError:
            status = 'error'
            error_message = "Scraping agotado (30 segundos)."
            print(f"Scraping agotado para URL: {url}")
        except aiohttp.ClientError as e:
            status = 'error'
            error_message = f"Error de cliente HTTP: {str(e)}"
            print(f"Error de cliente al hacer scraping de URL {url}: {e}")
        except Exception as e:
            status = 'error'
            error_message = str(e)
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


async def main():
    global PROCESSING_SERVER_IP, PROCESSING_SERVER_PORT
    parser = argparse.ArgumentParser(description="Servidor de Scraping Web Asíncrono")
    parser.add_argument('-i', '--ip', type=str, required=True, 
                        help="Dirección de escucha (soporta IPv4/IPv6)")
    parser.add_argument('-p', '--port', type=int, required=True, 
                        help="Puerto de escucha")
    parser.add_argument('-w', '--workers', type=int, default=4, 
                        help="Número de workers (default: 4) - Configuración para límite de conexiones concurrentes")
    parser.add_argument('--processing_ip', type=str, default=PROCESSING_SERVER_IP,
                        help=f"IP del servidor de procesamiento (default: {PROCESSING_SERVER_IP})")
    parser.add_argument('--processing_port', type=int, default=PROCESSING_SERVER_PORT,
                        help=f"Puerto del servidor de procesamiento (default: {PROCESSING_SERVER_PORT})")

    args = parser.parse_args()

    PROCESSING_SERVER_IP = args.processing_ip
    PROCESSING_SERVER_PORT = args.processing_port

    app = aiohttp.web.Application()
    app.router.add_get('/scrape', handle_scrape)

    print(f"Servidor de Scraping escuchando en {args.ip}:{args.port}")
    print(f"Conectando al servidor de procesamiento: {PROCESSING_SERVER_IP}:{PROCESSING_SERVER_PORT}")
    print(f"Workers configurados: {args.workers}")
    
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    
    # Crear sitio con soporte IPv4/IPv6
    site = aiohttp.web.TCPSite(runner, args.ip, args.port)
    await site.start()

    # Mantener el servidor corriendo hasta que se interrumpa
    try:
        print("Servidor iniciado. Presiona Ctrl+C para detener.")
        await asyncio.Event().wait()  # Esperar indefinidamente
    except KeyboardInterrupt:
        print("\n⏹ Servidor de Scraping detenido.")
    finally:
        await runner.cleanup()


if __name__ == '__main__':
    asyncio.run(main())
