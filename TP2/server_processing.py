import socketserver
import argparse
import os
from multiprocessing import Pool
from processor.image_processor import image_processor
from processor.performance import performance
from processor.screenshot import screenshot

# Variable global para el pool de procesos
PROCESS_POOL = None

# Socketserver para manejar solicitudes TCP y enviar respuestas
class TCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Recibir y procesar la solicitud
        data = str(self.request.recv(1024), 'ascii').strip()

        print("Solicitud recibida:", data)

        # Diccionario para comandos
        dispatch = {
            'image': image_processor,
            'screenshot': screenshot,
            'performance': performance,
        }

        try:
            # Dividir solicitud en comando y argumento (url)
            command, argument = data.split(',', 1)
            handler = dispatch.get(command) # Usar el handler correspondiente

            if handler: # Si es un comando valido

                # Enviar la tarea al pool de procesos
                # apply_async devuelve un objeto AsyncResult

                result = PROCESS_POOL.apply_async(handler, (argument,))
                
                # Esperar el resultado de la tarea. Esto bloquea el handler,
                # pero el servidor puede seguir aceptando nuevas conexiones.

                response = result.get()

            else:
                response = f"Error: Comando '{command}' desconocido.".encode('ascii')

        except ValueError:
            response = "Error: Formato de input invalido. Se esperaba 'comando,argumento'.".encode('ascii')
        
        except Exception as e:
            # Capturar cualquier excepcion del worker
            print(f"Error procesando la solicitud en el worker: {e}")
            response = f"Error interno del servidor: {e}".encode('ascii')

        self.request.sendall(response) # Enviar la respuesta correspondiente


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido")
    parser.add_argument("-i", "--ip", type=str, default="localhost",
                        help="Dirección de escucha")
    parser.add_argument("-p", "--port", type=int, default=8081,
                        help="Puerto de escucha")
    parser.add_argument("-n", "--processes", type=int, default=os.cpu_count(),
                        help="Numero de procesos en el pool (default: CPU count)")

    args = parser.parse_args()

    HOST, PORT = args.ip, args.port
    num_processes = args.processes

    # Inicializar el pool de procesos
    PROCESS_POOL = Pool(processes=num_processes)
    print(f"Pool de procesos inicializado con {num_processes} workers.")

    try:
        with socketserver.TCPServer((HOST, PORT), TCPRequestHandler) as server:
            server.allow_reuse_address = True
            print(f"Iniciando servidor de procesamiento en {HOST}:{PORT}...")
            server.serve_forever()
    except KeyboardInterrupt:
        print("Servidor detenido por el usuario.")
    finally:
        # Asegurarse de cerrar el pool de procesos
        if PROCESS_POOL:
            PROCESS_POOL.close()
            PROCESS_POOL.join()
            print("Pool de procesos cerrado.")