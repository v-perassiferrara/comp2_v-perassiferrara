import argparse
import socketserver
import multiprocessing
import os

from common.protocol import Protocol
from processor.screenshot import capture_screenshot
from processor.performance import analyze_performance
from processor.image_processor import process_images


# Funcion para ejecutar tareas de procesamiento en un proceso separado
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
        # self.request es el socket TCP conectado al cliente
        try:
            # Recibir longitud del mensaje
            length_bytes = self.request.recv(4)
            if not length_bytes:
                print("Cliente desconectado.")
                return

            message_length = Protocol.decode_length(length_bytes)
            message_bytes = self.request.recv(message_length)
            request_data = Protocol.decode_message(message_bytes)

            print(f"Solicitud recibida: {request_data}")

            url = request_data.get('url')
            if not url:
                response_data = {'status': 'error', 'message': 'URL no especificada'}
                encoded_response = Protocol.encode_message(response_data)
                self.request.sendall(encoded_response)
                return

            # Ejecutar tareas usando el pool de multiprocessing
            pool = self.server.pool

            # Definir tareas de procesamiento (se ejecutan en paralelo)
            processing_tasks = [
                pool.apply_async(run_processing_task, ('screenshot', url)),
                pool.apply_async(run_processing_task, ('performance', url)),
                pool.apply_async(run_processing_task, ('images', url))
            ]

            results = {}
            
            # Recolectar resultados con timeout
            for i, task in enumerate(processing_tasks):
                try:
                    if i == 0:  # Screenshot
                        results['screenshot'] = task.get(timeout=60)
                    elif i == 1:  # Performance
                        results['performance'] = task.get(timeout=60)
                    elif i == 2:  # Images
                        results['thumbnails'] = task.get(timeout=60)
                except multiprocessing.TimeoutError:
                    print(f"Tarea de procesamiento {i} agotada para URL: {url}")
                    if i == 0:
                        results['screenshot'] = None
                    elif i == 1:
                        results['performance'] = {'error': 'Timeout'}
                    elif i == 2:
                        results['thumbnails'] = []
                except Exception as e:
                    print(f"Error en tarea de procesamiento {i} para URL {url}: {e}")
                    if i == 0:
                        results['screenshot'] = None
                    elif i == 1:
                        results['performance'] = {'error': str(e)}
                    elif i == 2:
                        results['thumbnails'] = []

            response_data = {
                'status': 'success',
                'processing_data': results
            }

            encoded_response = Protocol.encode_message(response_data)
            self.request.sendall(encoded_response)

        except Exception as e:
            print(f"Error manejando solicitud: {e}")
            try:
                response_data = {'status': 'error', 'message': str(e)}
                encoded_response = Protocol.encode_message(response_data)
                self.request.sendall(encoded_response)
            except Exception:
                pass  # Si falla el envio, no hay mucho que hacer


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Servidor TCP con soporte para múltiples hilos"""
    allow_reuse_address = True  # Permite reutilizar la dirección inmediatamente


def main():
    parser = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido")
    parser.add_argument('-i', '--ip', type=str, required=True, 
                        help="Dirección de escucha")
    parser.add_argument('-p', '--port', type=int, required=True, 
                        help="Puerto de escucha")
    parser.add_argument('-n', '--processes', type=int, default=os.cpu_count(),
                        help=f"Número de procesos en el pool (default: {os.cpu_count()})")

    args = parser.parse_args()

    # Crear pool de procesos
    process_pool = multiprocessing.Pool(processes=args.processes)

    print("Servidor de Procesamiento iniciado")
    print(f"Escuchando en {args.ip}:{args.port}")
    print(f"Pool de {args.processes} procesos")

    server = None
    try:
        # Crear y configurar servidor
        server = ThreadedTCPServer((args.ip, args.port), ProcessingHandler)
        server.pool = process_pool  # Adjuntar pool al servidor

        print("Servidor listo. Presiona Ctrl+C para detener.")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n -- Servidor de Procesamiento detenido. --")
    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        # Limpieza ordenada de recursos
        if server:
            server.shutdown()
            server.server_close()
        
        print("Cerrando pool de procesos...")
        process_pool.close()
        process_pool.join()
        print("Pool de procesos cerrado correctamente.")


if __name__ == '__main__':
    main()
