# server_tcp_ipv6_echo.py
import socket


'''es lo mismo que antes pero por ipv6'''


HOST, PORT = "::1", 9301  # loopback IPv6   ("localhost")

with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(8)
    print(f"[TCP/IPv6] [{HOST}]:{PORT}")
    
    try:
        while True:
            conn, addr = srv.accept()  # addr es tupla IPv6 (ip, port, flowinfo, scopeid)

                    # "flowinfo es para Quality of Service (normalmente 0)"
                    # "scopeid identifica alcance de la dirección cuando la esta no es global"


            print("Conexión de", addr)
            with conn:
                while True:
                    b = conn.recv(4096) # recibe datos del cliente
                    if not b: 
                        break
                    conn.sendall(b) # envia de vuelta los mismos datos (eco)
            print("Cierre de", addr)
    except KeyboardInterrupt:
        print("\nServidor IPv6 detenido")