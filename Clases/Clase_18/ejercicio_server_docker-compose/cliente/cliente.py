import socket
import os
import time

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))

def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(bytes(message, 'ascii'), (ip, port))
        response, addr = sock.recvfrom(1024)
        print("Received: {}".format(response.decode('ascii')))
        
if __name__ == "__main__":
    while True:    
        client(SERVER_HOST, SERVER_PORT, "prueba mensaje")
        time.sleep(5)
        
        
# Para cliente externo al contenedor usar:  nc -u 0.0.0.0 9999