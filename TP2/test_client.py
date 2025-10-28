import socket
import sys

def run_client(host, port, message):
    """
    Se conecta a un servidor TCP, envía un mensaje y recibe una respuesta.
    """
    try:
        # Crear un socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Conectar al servidor
            sock.connect((host, port))

            # Enviar el mensaje codificado
            print(f"Enviando: '{message}'")
            sock.sendall(message.encode('ascii'))

            # Recibir la respuesta
            # Es importante manejar respuestas grandes que pueden no llegar en un solo paquete.
            response_parts = []
            while True:
                try:
                    # Establecemos un timeout para no quedar esperando indefinidamente
                    sock.settimeout(20.0)
                    data = sock.recv(4096)
                    if not data:
                        break # El servidor cerró la conexión
                    response_parts.append(data)
                except socket.timeout:
                    # Si se alcanza el timeout, asumimos que hemos recibido todo.
                    print("Timeout esperando más datos. Asumiendo fin de la respuesta.")
                    break
            
            response = b"".join(response_parts)

            # Procesar y mostrar la respuesta
            if len(response) > 200:
                 # Si la respuesta es larga (como una imagen en base64), la truncamos.
                print(f"Respuesta recibida (truncada): {response[:200]}...")
                print(f"Tamaño total de la respuesta: {len(response)} bytes")
            else:
                print(f"Respuesta recibida: {response.decode('ascii', errors='ignore')}")


    except ConnectionRefusedError:
        print(f"Error: La conexión fue rechazada. ¿Está el servidor corriendo en {host}:{port}?")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python test_client.py 'comando,url'")
        print("Ejemplo: python test_client.py 'screenshot,https://www.google.com'")
        sys.exit(1)

    HOST, PORT = "localhost", 8081
    message_to_send = sys.argv[1]
    
    run_client(HOST, PORT, message_to_send)
