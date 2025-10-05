'''
Ejercicio 2: Chat Simple

Objetivo: Crear un sistema de chat cliente-servidor usando IPv6.

Requisitos del servidor:

    Aceptar múltiples clientes simultáneamente
    Transmitir mensajes de un cliente a todos los demás
    Mostrar quién envía cada mensaje

Requisitos del cliente:

    Conectarse al servidor
    Permitir enviar y recibir mensajes en tiempo real

'''

import socketserver
import socket
import threading

clientes = []  # Lista compartida de sockets de clientes

class ManejadorThreading(socketserver.BaseRequestHandler):
    def handle(self):
        thread_name = threading.current_thread().name
        print(f"[{thread_name}] Conexión de: {self.client_address}")
        
        # Agregar cliente a la lista
        clientes.append(self.request)
        
        try:
            while True:
                data = self.request.recv(1024)
                if not data:
                    break
                
                mensaje = f"{self.client_address} envió: {data.decode()}"
                print(mensaje)
                
                # Broadcast a todos los clientes
                for cliente in clientes:
                    try:
                        cliente.sendall(mensaje.encode())
                    except:  # noqa: E722
                        clientes.remove(cliente)  # Borrar de la lista si falla
        finally:
            # Borrar cliente al desconectar
            if self.request in clientes:
                clientes.remove(self.request)
            print(f"[{thread_name}] Conexión cerrada")

class ServidorIPv6Threading(socketserver.ThreadingTCPServer):
    address_family = socket.AF_INET6
    allow_reuse_address = True

if __name__ == "__main__":
    HOST, PORT = "::", 9900
    servidor = ServidorIPv6Threading((HOST, PORT), ManejadorThreading)
    print(f"Servidor chat multi-hilo IPv6 en [{HOST}]:{PORT}")
    
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando servidor...")
        servidor.shutdown()