

# Server

# nc -u -l 127.0.0.1 9006

# Escribir respuesta manual “pong” cuando el cliente envíe “ping”
                        
                        # "pong" o cualquier cosa




# Cliente

import socket

HOST, PORT = "127.0.0.1", 9006

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    
    # en este caso usamos dgram (UDP) => no hay connect
    
    s.sendto(b"ping", (HOST, PORT)) # el cliente envia ping
    
    data, addr = s.recvfrom(2048)   # si recibe respuesta, la imprime
    
    # en send y en recv se indica direccion de destino y origen
    # porque no hubo connect previo
    
    print(f"< {data!r} desde {addr}")