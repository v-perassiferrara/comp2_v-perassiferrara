#Idea: Implementar un mini-protocolo textual: PING→PONG, ECHO <msg>, TIME.

#Cliente: 
# nc 127.0.0.1 9011



# Server

import socket
import time

HOST, PORT = "127.0.0.1", 9011  # puerto donde se establece el server

def handle_line(line: str) -> str:  # funcion que gestiona la respuesta segun el comando
    line = line.strip()
    
    if line == "PING":  # ping devuelve pong
        return "PONG\n"
    
    if line.startswith("ECHO "):    # echo devuelve lo que le sigue
        return line[5:] + "\n"
    
    if line == "TIME":  # time devuelve la hora actual
        return time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
    
    return "ERR desconocido\n"


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:  # socket pasivo inicial del servidor
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    srv.bind((HOST, PORT))  # fija la ip y puerto del servidor
    
    srv.listen(8)  # backlog de 8 conexiones (que puede atender el servidor)
    
    print(f"CMD en {HOST}:{PORT}")


    while True: # bucle de sesiones
                
        conn, addr = srv.accept()   # acepta una conexión de un cliente (crea socket activo)
        
        with conn, conn.makefile("rwb", buffering=0) as f:
            
            # en este caso, makefile convierte el socket en un objeto tipo archivo (file-like)
            # para leer/escribir fácilmente línea por línea.
            
            # rwb = lectura/escritura/buffering,
            # pero como buffering=0, se escribe directamente en el socket
            
            
            
            for raw in f:  # itera por líneas leidas (bloqueante)
                
                resp = handle_line(raw.decode("utf-8", "replace"))
                # por cada linea, gestiona la respuesta con handle_line
                
                f.write(resp.encode("utf-8"))   # manda la respuesta al cliente