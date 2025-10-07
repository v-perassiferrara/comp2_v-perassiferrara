import socket

# Crear socket IPv6
server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# Configurar para reutilizar la dirección
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Enlazar a dirección y puerto
# '::1' es "localhost" en IPv6
# '::' escucha en todas las interfaces
server_address = ('::1', 8080)  # como si pusieramos localhost:8080
server_socket.bind(server_address)

# Escuchar conexiones
server_socket.listen(5) # número máximo de conexiones que se pueden tener en cola
print(f"Servidor IPv6 escuchando en {server_address}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Conexión desde: {client_address}")
    
    # Recibir datos
    data = client_socket.recv(1024)
    print(f"Recibido: {data.decode()}")
    
    # Enviar respuesta
    response = f"Servidor recibió: {data.decode()}"
    client_socket.sendall(response.encode())
    
    client_socket.close()