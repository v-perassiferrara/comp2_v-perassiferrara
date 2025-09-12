'''
Ejercicio 1: Servidor de Archivos Básico

Crea un servidor HTTP que sirva archivos estáticos desde un directorio específico. El servidor debe:

    Responder a solicitudes GET
    Servir archivos HTML, CSS, JS e imágenes
    Mostrar un listado de directorio cuando se accede a una carpeta
    Devolver 404 para archivos inexistentes
'''

import http.server
import os

# El handler simple ya trae todo implementado
class FileServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=".", **kwargs):
        
        # Asegurar que existe el directorio
        if not os.path.exists(directory):
            os.makedirs(directory)

        super().__init__(*args, directory=directory, **kwargs)

if __name__ == "__main__":
    PORT = 8080
    
    with http.server.HTTPServer(("", PORT), FileServer) as httpd:
        print(f"Servidor ejecutándose en http://localhost:{PORT}")
        print("Sirviendo archivos desde ./public/")
        httpd.serve_forever()