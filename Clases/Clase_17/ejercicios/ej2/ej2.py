'''
Ejercicio 2: API REST Básica

Implementa un servidor que simule una API REST para gestionar una lista de users. Debe soportar:

    GET /users - Listar todos los users
    GET /users/id - Obtener un user específico
    POST /users - Crear un nuevo user
    PUT /users/id - Actualizar un user existente
    DELETE /users/id - Eliminar un user

Los datos pueden almacenarse en memoria (lista/diccionario).
'''

import http.server
import json
from urllib.parse import urlparse

class CustomHandler(http.server.BaseHTTPRequestHandler):

    users = ["Jorge", "Ana", "Luis", "María"]



    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/users':    # Para listar todos los users
            self._send_html_response(self.users.__str__())

        elif parsed_path.path.startswith('/users/'):    # Para ver users individuales

            user_id = parsed_path.path.split('/')[-1]   # Extraemos el ID (índice de la lista) de la URL
            
            if user_id.isdigit() and 0 <= int(user_id) < len(self.users):    # Validamos que ID sea un número y esté dentro del rango
                self._send_json_response({'user': self.users[int(user_id)]})
            else:
                self._send_error_response(404, 'user no encontrado')
        else:
            self._send_error_response(404, 'Página no encontrada')  # Para otra ruta, devolvemos error 404
    


    def do_POST(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/users':    # Para listar todos los users

            # Leemos el cuerpo de la solicitud
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length) # Lee exactamente el largo del contenido indicado en el header
            
            try:
                # Intentamos parsear como JSON
                data = json.loads(post_data.decode('utf-8'))
                
                if "user" in data:  # Verifico que exista el campo "user" en el JSON
                    
                    user_name = data["user"]  # Solo guardo el nombre del user
                    self.users.append(user_name)
                else:
                    self._send_error_response(400, 'El JSON debe contener el campo "user"')
                    return

                response_data = {
                    "message": "Usuario agregado a la lista",
                    "user_added": user_name,
                    "total_users": len(self.users),
                    "all_users": self.users
                }
                
                self._send_json_response(response_data)

            except json.JSONDecodeError:
                self._send_error_response(400, 'JSON inválido')
    
        else:
            self._send_error_response(404, 'Página no encontrada')  



    def do_PUT(self):
        
        # Parseamos URL para extraer ruta y parámetros
        parsed_path = urlparse(self.path)

        # Leemos el cuerpo de la solicitud
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        
        if parsed_path.path.startswith('/users/'):    # Para modificar un user

            user_id = parsed_path.path.split('/')[-1]   # Extraemos el ID a modificar (índice de la lista) de la URL
            
            if user_id.isdigit() and 0 <= int(user_id) < len(self.users):    # Validamos que ID sea un número y esté dentro del rango
                
                try:
                    # Intentamos parsear como JSON y modificar el user
                    data = json.loads(post_data.decode('utf-8'))
                    
                    if "user" in data:  # Verifico que exista el campo "user" en el JSON
                        
                        user_name = data["user"]  
                        self.users[int(user_id)] = user_name    # Reemplazo el user en la posición indicada
                    else:
                        self._send_error_response(400, 'El JSON debe contener el campo "user"')
                        return

                    response_data = {
                        "message": "Usuario modificado",
                        "user_modified": user_name,
                        "total_users": len(self.users),
                        "all_users": self.users
                    }
                    
                    self._send_json_response(response_data)

                except json.JSONDecodeError:
                    self._send_error_response(400, 'JSON inválido')

            else:
                self._send_error_response(404, 'user no encontrado')
        else:
            self._send_error_response(404, 'Página no encontrada')  # Para otra ruta, devolvemos error 404


    
    def do_DELETE(self):
        # Parseamos URL para extraer ruta y parámetros
        parsed_path = urlparse(self.path)

        
        if parsed_path.path.startswith('/users/'):    # Para borrar un user

            user_id = parsed_path.path.split('/')[-1]   # Extraemos el ID a borrar
            
            if user_id.isdigit() and 0 <= int(user_id) < len(self.users):    # Validamos que ID sea un número y esté dentro del rango
                       
                user_name = self.users.pop(int(user_id))    # Elimino el user en la posición indicada

                response_data = {
                    "message": "Usuario borrado de la lista",
                    "user_deleted": user_name,
                    "total_users": len(self.users),
                    "all_users": self.users
                }
                
                self._send_json_response(response_data)

            else:
                self._send_error_response(404, 'user no encontrado')
        else:
            self._send_error_response(404, 'Página no encontrada')  # Para otra ruta, devolvemos error 404


    def _send_html_response(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
    def _send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _send_error_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode())

# Iniciar servidor con threading para manejar múltiples conexiones
if __name__ == "__main__":
    PORT = 8080
    with http.server.ThreadingHTTPServer(("", PORT), CustomHandler) as httpd:
        print(f"Servidor ejecutándose en http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nCerrando servidor...")