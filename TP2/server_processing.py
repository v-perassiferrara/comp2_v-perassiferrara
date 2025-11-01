import argparse
import socketserver
import multiprocessing
import os
import signal
import sys

from common.protocol import Protocol
from processor.screenshot import capture_screenshot
from processor.performance import analyze_performance
from processor.image_processor import process_images


# Función para ejecutar tareas de procesamiento en un proceso separado
def run_processing_task(task_name, url, **kwargs):
    """Ejecuta una tarea de procesamiento en un proceso separado"""
    try:
        if task_name == 'screenshot':
            return capture_screenshot(url, **kwargs)
        elif task_name == 'performance':
            return analyze_performance(url, **kwargs)
        elif task_name == 'images':
            return process_images(url, **kwargs)
        else:
            raise ValueError(f"Tarea desconocida: {task_name}")
    except Exception as e:
        print(f"Error en la tarea {task_name}: {e}")
        return None


class ProcessingHandler(socketserver.BaseRequestHandler):
    """
    Handler para procesar solicitudes del servidor de scraping.
    Ejecuta tareas CPU-intensive en procesos separados.
    """

    def handle(self):
        """Maneja una conexión entrante"""
        try:
            # Recibir longitud del mensaje
            length_bytes = self.request.recv(4)
            if not length_bytes or len(length_bytes) < 4:
                print("Cliente desconectado o datos incompletos.")
                return

            message_length = Protocol.decode_length(length_bytes)
            
            # Recibir el mensaje completo
            message_bytes = b''
            while len(message_bytes) < message_length:
                chunk = self.request.recv(min(4096, message_length - len(message_bytes)))
                if not chunk:
                    print("Conexión cerrada antes de recibir el mensaje completo.")
                    return
                message_bytes += chunk
            
            request_data = Protocol.decode_message(message_bytes)
            print(f"Solicitud recibida de {self.client_address}: {request_data}")

            url = request_data.get('url')
            if not url:
                response_data = {'status': 'error', 'message': 'URL no especificada'}
                encoded_response = Protocol.encode_message(response_data)
                self.request.sendall(encoded_response)
                return

            # Ejecutar tareas usando el pool de multiprocessing
            pool = self.server.pool

            # Definir tareas de procesamiento (se ejecutan en paralelo)
            print(f"Iniciando procesamiento paralelo para URL: {url}")
            
            screenshot_task = pool.apply_async(run_processing_task, ('screenshot', url))
            performance_task = pool.apply_async(run_processing_task, ('performance', url))
            images_task = pool.apply_async(run_processing_task, ('images', url))

            results = {}
            
            # Recolectar resultados con timeout
            try:
                results['screenshot'] = screenshot_task.get(timeout=60)
            except multiprocessing.TimeoutError:
                print(f"Timeout en captura de screenshot para URL: {url}")
                results['screenshot'] = None
            except Exception as e:
                print(f"Error en captura de screenshot para URL {url}: {e}")
                results['screenshot'] = None

            try:
                results['performance'] = performance_task.get(timeout=60)
            except multiprocessing.TimeoutError:
                print(f"Timeout en análisis de rendimiento para URL: {url}")
                results['performance'] = {'error': 'Timeout'}
            except Exception as e:
                print(f"Error en análisis de rendimiento para URL {url}: {e}")
                results['performance'] = {'error': str(e)}

            try:
                results['thumbnails'] = images_task.get(timeout=60)
            except multiprocessing.TimeoutError:
                print(f"Timeout en procesamiento de imágenes para URL: {url}")
                results['thumbnails'] = []
            except Exception as e:
                print(f"Error en procesamiento de imágenes para URL {url}: {e}")
                results['thumbnails'] = []

            print(f"Procesamiento completado para URL: {url}")

            response_data = {
                'status': 'success',
                'processing_data': results
            }

            encoded_response = Protocol.encode_message(response_data)
            self.request.sendall(encoded_response)

        except ConnectionResetError:
            print("Conexión reiniciada por el cliente.")
        except BrokenPipeError:
            print("Pipe roto: el cliente cerró la conexión.")
        except Exception as e:
            print(f"Error manejando solicitud: {e}")
            try:
                response_data = {'status': 'error', 'message': str(e)}
                encoded_response = Protocol.encode_message(response_data)
                self.request.sendall(encoded_response)
            except Exception:
                pass  # Si falla el envío, no hay mucho que hacer


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Servidor TCP con soporte para múltiples hilos"""
    allow_reuse_address = True
    daemon_threads = True  # Los hilos daemon se terminan cuando el programa principal termina


def signal_handler(signum, frame):
    """Manejador de señales para cierre limpio"""
    print("\n -- Señal recibida, cerrando servidor... --")
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido")
    parser.add_argument('-i', '--ip', type=str, required=True, 
                        help="Dirección de escucha")
    parser.add_argument('-p', '--port', type=int, required=True, 
                        help="Puerto de escucha")
    parser.add_argument('-n', '--processes', type=int, default=os.cpu_count(),
                        help=f"Número de procesos en el pool (default: {os.cpu_count()})")

    args = parser.parse_args()

    # Validar número de procesos
    if args.processes < 1:
        print("Error: El número de procesos debe ser al menos 1")
        return

    # Configurar manejadores de señales
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)

    # Crear pool de procesos
    print(f"Creando pool de {args.processes} procesos...")
    process_pool = multiprocessing.Pool(processes=args.processes)

    print("\n=== Servidor de Procesamiento ===")
    print(f"Escuchando en {args.ip}:{args.port}")
    print(f"Pool de {args.processes} procesos workers")
    print("================================\n")

    server = None
    try:
        # Crear y configurar servidor
        server = ThreadedTCPServer((args.ip, args.port), ProcessingHandler)
        server.pool = process_pool  # Adjuntar pool al servidor

        print("Servidor listo para recibir conexiones.")
        print("Presiona Ctrl+C para detener.\n")
        
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n -- Servidor detenido por el usuario. --")
    except OSError as e:
        print(f"Error al iniciar el servidor: {e}")
        if "Address already in use" in str(e):
            print(f"El puerto {args.port} ya está en uso. Intenta con otro puerto.")
    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        # Limpieza ordenada de recursos
        print("\nCerrando recursos...")
        
        if server:
            try:
                server.shutdown()
                server.server_close()
                print("Servidor cerrado.")
            except Exception as e:
                print(f"Error cerrando servidor: {e}")
        
        print("Cerrando pool de procesos...")
        try:
            process_pool.close()
            process_pool.join(timeout=5)
            print("Pool de procesos cerrado correctamente.")
        except Exception as e:
            print(f"Error cerrando pool: {e}")
            process_pool.terminate()
            process_pool.join()


if __name__ == '__main__':
    # Para multiprocessing en Windows
    multiprocessing.freeze_support()
    main()
