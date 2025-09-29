import socketserver
from datetime import datetime

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    Handler para nuestro servidor UDP.
    La lógica aquí es correcta para el manejo de datagramas.
    """

    def handle(self):
        # Desempaquetar self.request para UDP
        data = self.request[0]
        socket = self.request[1]
        
        print(f"Recibido de {self.client_address}:")
        print(data.decode('utf-8'))

        # 2. Usar el socket del servidor para ENVIAR DE VUELTA al cliente
        # El método es .sendto(data, address)
        socket.sendto(str(datetime.now()).encode('utf-8'), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    # La forma correcta de establecer opciones como allow_reuse_address
    # es a menudo creando una subclase del servidor.
    class ReusableUDPServer(socketserver.UDPServer):
        allow_reuse_address = True

    print(f"Servidor UDP de hora iniciado en {HOST}:{PORT}")
    
    # Usamos nuestra clase de servidor personalizada
    with ReusableUDPServer((HOST, PORT), MyUDPHandler) as server:
        # El servidor se ejecuta hasta que lo interrumpas con Ctrl+C
        server.serve_forever()