# Cliente

# nc 127.0.0.1 9010



# Server

import socket

HOST, PORT = "127.0.0.1", 9010

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:  # socket pasivo TCP inicial del servidor

    # Permite reusar el puerto de inmediato al reiniciar el servidor.
    # Sin esto, el sistema operativo lo bloquea en estado TIME_WAIT para procesar paquetes tardíos, 
    # lo que causaría un error de "Address already in use".
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    srv.bind((HOST, PORT))  # fija la ip y puerto del servidor
    
    srv.listen(8)  # backlog de 8 conexiones (que puede atender el servidor)
    
    print(f"Escuchando en {HOST}:{PORT} ... Ctrl+C para salir") # hace un listen


    while True:  # loop de sesiones (secuenciales)
        
        conn, addr = srv.accept()    # acepta una conexión de un cliente (crea socket activo)
        
        print("Conexión de", addr)
        
        with conn:
            while True:
                b = conn.recv(4096) # si conecta, intenta recibir algo
                if not b:   # si no recibe nada, es porque el cliente cerró ==> termina la sesión
                    break  # peer cerró
                conn.sendall(b)  # eco -> reenvía lo recibido
                
        print("Cierre de", addr)
        
        # quit() # cerraria el server al terminar una sesión