import socket
import os
import time

SOCKET_PATH = "/tmp/eco.sock"

def main():
    if not os.path.exists(SOCKET_PATH):
        raise SystemExit(f"No existe {SOCKET_PATH}. ¿Arrancaste `nc -lU {SOCKET_PATH}`?")
    
    # En este caso el netcat hace de servidor,
    # "escuchando" (-l) en el socket unix (-U) hasta que llegue algo.



    # AF_UNIX = dominio local (archivo-socket), STREAM = estilo TCP, no es TCP porque es un socket unix
    
    # El manejador de contexto (with ...) es aplicable a sockets también, 
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(SOCKET_PATH)
        s.sendall(b"hola desde UDS\n")
        # `nc` no hace eco automático, pero podés teclear algo y ENTER en la terminal del nc
        # para que el cliente lo lea. Si no hay datos, recv puede bloquear.
        for _ in range(2):
            time.sleep(1)
            data = s.recv(4) # el mensaje se divide en "bloques" de 4 bytes
            print(f"< {data!r}")

if __name__ == "__main__":
    main()