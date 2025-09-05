# server_tcp_ipv4_cmd.py
import socket
import time

HOST, PORT = "127.0.0.1", 9102

def handle(line: str) -> str:   # procesa un comando y devuelve la respuesta
    line = line.strip()
    if line == "PING":  # ping devuelve pong
        return "PONG\n"
    if line.startswith("ECHO "):    # echo devuelve lo que le siga
        return line[5:] + "\n"
    if line == "TIME":  # time devuelve la hora actual
        return time.strftime("%Y-%m-%d %H:%M:%S") + "\n"    
    return "ERR\n"  # comando no reconocido ==> error

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(8)
    print(f"[TCP/IPv4 CMD] {HOST}:{PORT}")

    try:
        while True:
            conn, addr = srv.accept()
            print("Conexión de", addr)
            with conn, conn.makefile("rwb", buffering=0) as f:
                for raw in f:
                    resp = handle(raw.decode("utf-8", "replace"))   # lee linea por linea lo que recibio
                    f.write(resp.encode("utf-8"))   # devuelve la respuesta
            print("Cierre de", addr)
    except KeyboardInterrupt:
        print("\nServidor detenido")