'''
Ejercicio 4: Servidor Dual Stack Inteligente

Objetivo: Crear un servidor que funcione con IPv4 e IPv6 y registre estadísticas.

Requisitos:

    Aceptar conexiones IPv4 e IPv6
    Llevar registro de:
        Número de conexiones por protocolo
        Tiempo promedio de respuesta
        Datos transferidos
    Generar un reporte al finalizar
'''

import socket
import socketserver
import threading
import time


estadisticas = {
    'ipv4': {'conexiones': 0, 'tiempo_medio_respuesta': 0, 'bytes_enviados': 0},
    'ipv6': {'conexiones': 0, 'tiempo_medio_respuesta': 0, 'bytes_enviados': 0}
}

lock = threading.Lock()


class ManejadorUniversal(socketserver.BaseRequestHandler):

    

    def handle(self):
        
        tiempos_respuesta = []
        
        # Detectar tipo de conexión
        if self.client_address[0].count(':') > 1:   # si hay dos puntos, es IPv6
            protocolo = "ipv6"
        else:
            protocolo = "ipv4"
        
        with lock:
            estadisticas[protocolo]['conexiones'] += 1
            
        
        print(f"[{protocolo}] Conexión de: {self.client_address}")
        
        
        tiempo_inicio = time.time()
        data = self.request.recv(1024).strip()        
        
        if not data:
            return
        
        respuesta = f"Servidor {protocolo}: {data.decode()}"
        self.request.sendall(respuesta.encode())

        tiempo_fin = time.time()
        
        tiempos_respuesta.append(tiempo_fin - tiempo_inicio)
        
        
        with lock:
            estadisticas[protocolo]['bytes_enviados'] += len(respuesta)
            estadisticas[protocolo]['tiempo_medio_respuesta'] = (sum(tiempos_respuesta)/len(tiempos_respuesta))



class ServidorIPv4(socketserver.ThreadingTCPServer):
    address_family = socket.AF_INET
    allow_reuse_address = True

class ServidorIPv6(socketserver.ThreadingTCPServer):
    address_family = socket.AF_INET6
    allow_reuse_address = True


def iniciar_servidor(familia, host, port, handler):
    
    # dependiendo del tipo de conexión, se usa un server IPv4 o IPv6
    
    """Inicia un servidor en un hilo separado"""
    if familia == socket.AF_INET:
        servidor = ServidorIPv4((host, port), handler)
        nombre = "IPv4"
    else:
        servidor = ServidorIPv6((host, port), handler)
        nombre = "IPv6"
    
    print(f"Iniciando servidor {nombre} en {host}:{port}")
    thread = threading.Thread(target=servidor.serve_forever, daemon=True)
    thread.start()
    return servidor, thread





if __name__ == "__main__":
    PORT = 9999
    servidores = []
    
    
    # Obtener direcciones disponibles
    direcciones = socket.getaddrinfo(None, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM)
    
    # None acá permite obtener todas las direcciones disponibles, ya que no especifica donde escuchar,
    # entonces escucha en todas las interfaces disponibles
        
    
    # Iniciar servidor para cada familia de direcciones
    familias_iniciadas = set()
    
    
    for addr_info in direcciones:
        familia = addr_info[0]
        if familia not in familias_iniciadas:
            host = "127.0.0.1" if familia == socket.AF_INET else "::1"
            
            srv, thread = iniciar_servidor(familia, host, PORT, ManejadorUniversal)
            
            servidores.append(srv)
            familias_iniciadas.add(familia)
    
    print("\nServidores iniciados. Presiona Ctrl+C para detener.")
    
    try:
        for srv in servidores:
            srv.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo servidores...")
        
        print("\nRegistro de estadísticas:")
        print("IPv4: ", estadisticas['ipv4'])
        print("IPv6: ", estadisticas['ipv6'])
        
        for srv in servidores:
            srv.shutdown()