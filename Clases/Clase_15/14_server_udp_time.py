# Idea: Si recibe TIME, responde la hora; en otro caso contesta ERR.

#Cliente: 
# nc -u 127.0.0.1 9014

# -u lo hace UDP



# Server

import socket
import time

HOST, PORT = "0.0.0.0", 9014

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:  # socket UDP
    s.bind((HOST, PORT))
    print(f"UDP TIME en {HOST}:{PORT}")
    
    while True:
        
        data, addr = s.recvfrom(2048)   # intenta recibir datos de alguien (bloqueante)
        
        msg = data.decode("utf-8", "replace").strip()   # decodifica y limpia el mensaje
        
        if msg == "TIME":   # si recibe TIME, responde la hora
            s.sendto(time.strftime("%H:%M:%S").encode(), addr)
            
        else:   # en otro caso contesta ERR
            s.sendto(b"ERR\n", addr)