

# Server

# Arrancarlo más tarde para forzar reintentos
# nc -l 127.0.0.1 9004




# Cliente

import socket
import time

HOST, PORT = "127.0.0.1", 9004

def try_connect(max_retries=5, base_backoff=0.5):
    '''
    al llamar la función, indicamos el número máximo de reintentos
    y el tiempo de espera entre cada uno
    '''
        
    for attempt in range(1, max_retries + 1):   # bucle de reintentos
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                
                s.settimeout(1.5)  # máximo tiempo de espera para la conexión
                
                s.connect((HOST, PORT))
                s.sendall(b"ping\n")
                data = s.recv(1024)
                return data
            
            
        except (socket.timeout, ConnectionRefusedError) as e:
            # si se supera el timeout, salta error,
            
            sleep_s = base_backoff * attempt   
            # el tiempo de espera se va incrementando con cada error
            
            print(f"Intento {attempt} falló ({e}). Reintento en {sleep_s:.1f}s...")
            
            time.sleep(sleep_s) # espera para luego reintentar
                                # (bucle for al principio)
            
            
    raise TimeoutError("Servidor no disponible tras varios reintentos")

                        # si no logra conectar tras el max_retries, lanza error


    # si el server no envia nada, termina dando error porque el cliente espera
    # respuesta, pero no llega, por lo que se supera el timeout


if __name__ == "__main__":
    print(try_connect())