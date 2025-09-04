

# Server

# nc -l 127.0.0.1 9003 < archivo_grande.bin




# Cliente

import socket

def recv_all(sock):   
      
    '''
    esta función ejecuta un bucle hasta lograr recibir todos los datos,
    de a 64 kb por vez, y los une en un solo bloque, que retorna
    '''
    
    chunks = []
    while True:
        b = sock.recv(300000)  # 64 KiB por iteración
        if not b:
            break
        # print("ejecutó recv()")
        chunks.append(b)
    return b"".join(chunks)


def main():     # usa un socket de internet (af_inet) con TCP (sock_stream)
    
    
    HOST, PORT = "127.0.0.1", 9003
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        
        data = recv_all(s)  # en lugar de s.recv() llama a recv_all
                            # con el que puede recibir todo lo que envíe el servidor
        
        print(f"Recibidos {len(data)} bytes")   # printea cuánto se recibió


if __name__ == "__main__":
    main()