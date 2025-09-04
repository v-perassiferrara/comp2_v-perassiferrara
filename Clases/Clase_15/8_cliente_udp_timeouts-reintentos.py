

# Server

# Arrancarlo más tarde para forzar reintentos
# nc -u -l 127.0.0.1 9007




# Cliente

import socket

HOST, PORT = "127.0.0.1", 9007

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    
    
    s.settimeout(1.0)   # tiempo máximo de espera de respuesta
    
    retries = 3 # numero maximo de reintentos si no hay respuesta
    
    
    for i in range(1, retries + 1): # bucle hasta 3 veces
        try:
            s.sendto(b"TIME", (HOST, PORT))
            
            
            data, _ = s.recvfrom(2048)  # si no llega nada, se supera el timeout
            
            
            print("Respuesta:", data.decode())
            break
        
        
        except socket.timeout:  # si se supera el timeout, salta error
            print(f"Timeout intento {i}; reintentando...")
            
    # si el server no envia nada, termina dando error porque el cliente espera
    # respuesta, pero no llega, por lo que se supera el timeout            
            
    else:
        print("Sin respuesta tras reintentos")