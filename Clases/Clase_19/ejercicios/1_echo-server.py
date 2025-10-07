import socketserver
import socket

class MiManejador(socketserver.BaseRequestHandler):
    def handle(self):
        # Información del cliente
        print(f"Conexión de: {self.client_address}")
        
        while True:
            # Recibir datos
            data = self.request.recv(1024).strip()
            if data == b"QUIT":
                self.request.sendall("Saliendo...\n".encode())
                self.request.close()
                break
            else:
                print(f"Recibido: {data.decode()}")
                # Enviar respuesta
                respuesta = f"Echo: {data.decode().upper()}"
                self.request.sendall(respuesta.encode())

# Crear clase de servidor IPv6
class ServidorIPv6(socketserver.TCPServer):
    address_family = socket.AF_INET6    # usamos socket de IPv6
    allow_reuse_address = True  # permite reusar la direccion

if __name__ == "__main__":
    HOST, PORT = "::1", 8888
    
    with ServidorIPv6((HOST, PORT), MiManejador) as servidor:
        print(f"Servidor IPv6 iniciado en [{HOST}]:{PORT}")
        servidor.serve_forever()