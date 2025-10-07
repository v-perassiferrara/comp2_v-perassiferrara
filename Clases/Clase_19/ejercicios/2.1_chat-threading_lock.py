import socketserver
import socket
import threading

clientes = set()  # Set compartido de sockets de clientes
clientes_lock = threading.Lock()  # Lock para acceso thread-safe

class ManejadorThreading(socketserver.BaseRequestHandler):
    def handle(self):
        thread_name = threading.current_thread().name
        print(f"[{thread_name}] Conexión de: {self.client_address}")
        
        # Agregar cliente al set
        with clientes_lock:
            clientes.add(self.request)
        
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            
            mensaje = f"{self.client_address} envió: {data.decode()}"
            print(mensaje)
            
            # Broadcast a todos los clientes
            with clientes_lock:
                for cliente in list(clientes):
                    try:
                        cliente.sendall(mensaje.encode())
                    except:  # noqa: E722
                        clientes.discard(cliente)  # Borrar si falla
        
        # Borrar cliente al desconectar
        with clientes_lock:
            if self.request in clientes:
                clientes.discard(self.request)
        print(f"[{thread_name}] Conexión cerrada")

class ServidorIPv6Threading(socketserver.ThreadingTCPServer):
    address_family = socket.AF_INET6
    allow_reuse_address = True

if __name__ == "__main__":
    HOST, PORT = "::1", 9900
    servidor = ServidorIPv6Threading((HOST, PORT), ManejadorThreading)
    
    print(f"Servidor chat multi-hilo IPv6 en [{HOST}]:{PORT}")
    
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando servidor...")
        servidor.shutdown()