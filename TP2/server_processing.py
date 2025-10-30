import argparse
import socketserver
import multiprocessing
import functools
import asyncio
import os
import sys

# Add the project root to the sys.path to allow imports from common and processor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.protocol import Protocol
from common.serialization import serialize, deserialize
from processor.screenshot import capture_screenshot
from processor.performance import analyze_performance
from processor.image_processor import process_images


# Function to run processing tasks in a separate process
def run_processing_task(task_name, url, **kwargs):
    if task_name == 'screenshot':
        return capture_screenshot(url, **kwargs)
    elif task_name == 'performance':
        return analyze_performance(url, **kwargs)
    elif task_name == 'images':
        return process_images(url, **kwargs)
    else:
        raise ValueError(f"Unknown task: {task_name}")

class ProcessingHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        try:
            # Receive message length
            length_bytes = self.request.recv(4)
            if not length_bytes:
                print("Client disconnected.")
                return

            message_length = Protocol.decode_length(length_bytes)
            message_bytes = self.request.recv(message_length)
            request_data = Protocol.decode_message(message_bytes)

            print(f"Received request: {request_data}")

            url = request_data.get('url')
            if not url:
                response_data = {'status': 'error', 'message': 'Missing URL'}
                encoded_response = Protocol.encode_message(response_data)
                self.request.sendall(encoded_response)
                return

            # Execute tasks using the multiprocessing pool
            # The pool is passed to the handler implicitly through the server object
            pool = self.server.pool

            # Define processing tasks
            processing_tasks = [
                pool.apply_async(run_processing_task, ('screenshot', url)),
                pool.apply_async(run_processing_task, ('performance', url)),
                pool.apply_async(run_processing_task, ('images', url))
            ]

            results = {}
            for i, task in enumerate(processing_tasks):
                try:
                    if i == 0:  # Screenshot
                        results['screenshot'] = task.get(timeout=60) # Increased timeout
                    elif i == 1: # Performance
                        results['performance'] = task.get(timeout=60)
                    elif i == 2: # Images
                        results['thumbnails'] = task.get(timeout=60)
                except multiprocessing.TimeoutError:
                    print(f"Processing task timed out for URL: {url}")
                    # Assign an error status or empty data for timed-out tasks
                    if i == 0: results['screenshot'] = None
                    elif i == 1: results['performance'] = {'error': 'Timed out'}
                    elif i == 2: results['thumbnails'] = []
                except Exception as e:
                    print(f"Error in processing task for URL {url}: {e}")
                    # Assign an error status or empty data for failed tasks
                    if i == 0: results['screenshot'] = None
                    elif i == 1: results['performance'] = {'error': str(e)}
                    elif i == 2: results['thumbnails'] = []

            response_data = {
                'status': 'success',
                'processing_data': results
            }

            encoded_response = Protocol.encode_message(response_data)
            self.request.sendall(encoded_response)

        except Exception as e:
            print(f"Error handling request: {e}")
            response_data = {'status': 'error', 'message': str(e)}
            encoded_response = Protocol.encode_message(response_data)
            self.request.sendall(encoded_response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass # No need for custom implementation here

def main():
    parser = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido")
    parser.add_argument('-i', '--ip', type=str, required=True, help="Dirección de escucha")
    parser.add_argument('-p', '--port', type=int, required=True, help="Puerto de escucha")
    parser.add_argument('-n', '--processes', type=int, default=os.cpu_count(),
                        help=f"Número de procesos en el pool (default: {os.cpu_count()})")

    args = parser.parse_args()

    # Create a pool of processes
    process_pool = multiprocessing.Pool(processes=args.processes)

    with ThreadedTCPServer((args.ip, args.port), ProcessingHandler) as server:
        # Add the pool to the server instance to make it accessible to handlers
        server.pool = process_pool

        print(f"Servidor de Procesamiento escuchando en {args.ip}:{args.port} con {args.processes} procesos.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Servidor de Procesamiento detenido.")
        finally:
            process_pool.close()
            process_pool.join()
            server.shutdown()

if __name__ == '__main__':
    main()
