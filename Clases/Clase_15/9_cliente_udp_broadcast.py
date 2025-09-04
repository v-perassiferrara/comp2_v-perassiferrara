# Server

# Escuchar en todas las interfaces
# nc -u -l 0.0.0.0 9008



# Cliente

import socket

PORT = 9008
BROADCAST = ("255.255.255.255", PORT)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s: # Datagrama ==> UDP
    
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # permite envio de broadcast
    
    s.settimeout(5.0)   # timeout para recibir respuesta
    
    s.sendto(b"DISCOVER?", BROADCAST)   # manda un broadcast a todas las IPs de la red local
    
    try:
        data, addr = s.recvfrom(4096)   # intenta recibir respuesta, si se supera el timeout -> excepción
        print(f"{addr} -> {data!r}")
    except socket.timeout:
        print("Nadie respondió al broadcast (o la red lo filtra)")