import socket

def obtener_direcciones(host, puerto):
    """Obtiene todas las direcciones disponibles para un host"""
    direcciones = socket.getaddrinfo(
        host, 
        puerto, 
        socket.AF_UNSPEC,  # IPv4 o IPv6
        socket.SOCK_STREAM  # TCP
    )
    
    for addr in direcciones:
        familia, tipo, proto, canonname, sockaddr = addr
        
        
        # para verificar si es IPv4 o IPv6 (AF_INET o AF_INET6)
        protocolo = "IPv4" if familia == socket.AF_INET else "IPv6"
        
        
        print(f"{protocolo}: {sockaddr}")
    
    return direcciones

# Ejemplo de uso

# en este caso, al indicar localhost, se usa IPv4
direcciones = obtener_direcciones("localhost", 8080)


# si en cambio usamos ::1, se usa IPv6
direcciones2 = obtener_direcciones("::1", 8080)