# Idea: Cerrar conexiones “colgadas” para liberar recursos.

#Cliente: 
# nc 127.0.0.1 9012



# Server

import socket

HOST, PORT = "127.0.0.1", 9012
IDLE_TIMEOUT = 5  # segundos de inactividad para cortar la conexión

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:  # socket pasivo inicial del servidor
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))  
    srv.listen(8)
    print(f"Timeout server en {HOST}:{PORT} (IDLE={IDLE_TIMEOUT}s)")

    while True:
        conn, addr = srv.accept()    # acepta una conexión de un cliente (crea socket activo)
        with conn:
            
            conn.settimeout(IDLE_TIMEOUT)   # establece el timeout de inactividad
            
            try:
                while True:
                    b = conn.recv(4096) # si conecta, intenta recibir datos
                    
                    if not b:   # si no recibe nada, es porque el cliente cerró ==> termina la sesión
                        break
                    
                    conn.sendall(b) # eco de vuelta
                    
            except socket.timeout:
                print("Inactividad excedida para", addr) # si se pasa del timeout, termina la sesión
                # cierre implícito al salir del with