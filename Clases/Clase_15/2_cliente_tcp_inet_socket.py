import socket

def main():
    HOST, PORT = "127.0.0.1", 9001
    # AF_INET = IPv4, SOCK_STREAM = TCP
    
    # Se usa casi igual que un socket de unix,
    # pero en lugar de con un archivo, con una dirección IP y un puerto.
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))                # 3-way handshake TCP
        s.sendall(b"hola mundo\n")            # envío atómico (o en fragmentos internos)
        data = s.recv(4096)                    # bloquea hasta recibir algo o cerrar
        print(f"< {data!r}")

if __name__ == "__main__":
    main()