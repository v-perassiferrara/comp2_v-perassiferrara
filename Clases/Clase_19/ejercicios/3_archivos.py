import socketserver
import socket
import os



'''
Hecho con ia. Si no veía cómo se tenía que hacer, no se me ocurría.
'''








'''
Ejercicio 3: Servidor de Archivos

Objetivo: Implementar un servidor que permita descargar archivos usando IPv6.

Requisitos:

    Listar archivos disponibles en un directorio
    Permitir al cliente solicitar archivos por nombre
    Transferir archivos de forma segura
    Manejar archivos grandes en chunks
'''







DIRECTORIO_ARCHIVOS = "./archivos"

class MiManejador(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Conexión de: {self.client_address}")
        try:
            while True:
                # Recibir comando (máx. 256 bytes para evitar abuso)
                data = self.request.recv(256).decode().strip()
                if not data:
                    return

                partes = data.split(maxsplit=1)
                comando = partes[0]

                if comando == "ls":
                    try:
                        archivos = os.listdir(DIRECTORIO_ARCHIVOS)
                        respuesta = "\n".join(archivos) + "\n"
                        self.request.sendall(respuesta.encode())
                    except Exception:
                        self.request.sendall(b"ERROR: No se pudo listar archivos\n")

                elif comando == "get" and len(partes) == 2:
                    nombre_archivo = partes[1].strip()

                    # Prevenir path traversal (básico)
                    if '/' in nombre_archivo or '\\' in nombre_archivo or nombre_archivo.startswith('.'):
                        self.request.sendall(b"ERROR: Nombre de archivo invalido\n")
                        return

                    ruta = os.path.join(DIRECTORIO_ARCHIVOS, nombre_archivo)
                    if os.path.isfile(ruta):
                        self.request.sendall(b"OK\n")
                        with open(ruta, "rb") as f:
                            while chunk := f.read(4096):
                                self.request.sendall(chunk)
                    else:
                        self.request.sendall(b"ERROR: Archivo no encontrado\n")
                else:
                    self.request.sendall(b"ERROR: Comando no reconocido. Usa 'ls' o 'get <archivo>'\n")

        except Exception as e:
            print(f"Error: {e}")
            self.request.sendall(b"ERROR: Solicitud invalida\n")

class ServidorIPv6(socketserver.TCPServer):
    address_family = socket.AF_INET6

if __name__ == "__main__":
    HOST, PORT = "::1", 9990
    os.makedirs(DIRECTORIO_ARCHIVOS, exist_ok=True)
    print(f"Servidor IPv6 iniciado en [{HOST}]:{PORT}")
    with ServidorIPv6((HOST, PORT), MiManejador) as servidor:
        servidor.serve_forever()