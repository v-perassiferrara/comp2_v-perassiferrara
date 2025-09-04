# Idea: Responder al remitente con lo mismo que envía; no hay conexiones.

#Cliente: 
# nc -u 127.0.0.1 9013

# -u lo hace UDP



# Server

import socket

HOST, PORT = "0.0.0.0", 9013

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s: # socket UDP
    
    s.bind((HOST, PORT))    # fija la ip y puerto del servidor
    
    # no hace listen ni accept, no hay conexiones
    
    print(f"UDP eco en {HOST}:{PORT}")
    
    
    while True:
        
        data, addr = s.recvfrom(4096)   # intenta recibir datos de alguien (bloqueante)
        
        print(f"{addr} -> {data!r}")
        
        s.sendto(data, addr)    # reenvía lo recibido al remitente original