import socket
import argparse
import json
import sys
import time

from src.shared.utils import DEFAULT_HOST, DEFAULT_PORT, BUFFER_SIZE


def main():
    # Seteamos argparse para recibir los argumentos

    parser = argparse.ArgumentParser(
        description="Cliente para el Sistema Distribuido de Análisis de Chats."
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="Ruta al archivo de chat (.txt) a procesar.",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=DEFAULT_HOST,
        help=f"Host del servidor (default: {DEFAULT_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Puerto del servidor (default: {DEFAULT_PORT})",
    )
    args = parser.parse_args()

    # Logica para determinar si usar IPv4 o IPv6 cuando no se especifica host

    host = args.host if args.host is not None else "localhost"

    port = args.port

    # Leer el archivo de chat del input
    try:
        with open(args.filepath, "r", encoding="utf-8") as f:
            file_content = f.read()

        if not file_content:
            print(f"Error: El archivo '{args.filepath}' está vacío.")
            sys.exit(1)

        # Codificamos para enviar por socket
        file_data = file_content.encode("utf-8")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en '{args.filepath}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        sys.exit(1)

    # Conectar al server por TCP y mandar el archivo
    sock = None
    last_error = None
    try:
        addr_info = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        # Esto trae todas las "recetas" (protocolos y direcciones) posibles para conectar al host y puerto indicados

        for family, socktype, proto, _, sockaddr in addr_info:
            try:
                sock = socket.socket(family, socktype, proto)
                print(f"Intentando conectar a {sockaddr}...")

                sock.settimeout(5)  # Timeout de 5 segundos

                sock.connect(sockaddr)

                sock.settimeout(None)  # Sin timeout para el resto de operaciones

                print(f"Conexión exitosa a {sockaddr}.")
                break
 
            except socket.error as e:  # Si salta error en alguno, lo guardamos y probamos la siguiente direccion
                last_error = e
                if sock:
                    sock.close()
                sock = None
                continue

        if sock is None:  # Si el bucle termina sin conexión, lanzamos el ultimo error
            if last_error:
                raise last_error
            else:
                raise socket.error("No se pudo resolver el host.")

        # Uso with para que el socket se cierre al final
        with sock:
            start_time = time.time()  # Para medir el tiempo total

            # Enviar archivo
            print(f"Enviando archivo '{args.filepath}' ({len(file_data)} bytes)...")
            sock.sendall(file_data)

            # Cierra la escritura (envia EOF, asi el server no queda bloqueado)
            print("Archivo enviado. Cerrando escritura en el socket...")
            sock.shutdown(socket.SHUT_WR)

            # Recibir Respuesta (estadisticas en JSON)
            print("Esperando respuesta del servidor...")
            response_chunks = []

            # Bucle para recibir toda la respuesta del server
            while True:
                chunk = sock.recv(BUFFER_SIZE)
                if not chunk:
                    break  # El servidor cerró la conexión
                response_chunks.append(chunk)

            response_data = b"".join(response_chunks).decode("utf-8")

            total_time = time.time() - start_time
            print(f"Respuesta recibida en {total_time:.2f} segundos.")

            # Mostrar resultados en consola (legibles)
            try:
                final_json = json.loads(response_data)
                print("\n--- Estadísticas Recibidas ---")
                print(json.dumps(final_json, indent=2, ensure_ascii=False))

            except json.JSONDecodeError:
                print("\n--- Respuesta Inválida (No es JSON) ---")
                print(response_data)

    except socket.error as e:
        print(f"\nError de Socket: {e}")
        print(f"¿Está el servidor corriendo en '{host}':'{port}'?")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
