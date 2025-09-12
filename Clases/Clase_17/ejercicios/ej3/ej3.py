'''
Ejercicio 3: Servidor de Formularios

Crea un servidor que:

    Sirva un formulario HTML en GET /
    Procese los datos del formulario en POST /submit
    Muestre una página de confirmación con los datos recibidos
    Maneje diferentes tipos de input (text, email, select, checkbox)
'''

import http.server
import json
from urllib.parse import urlparse, parse_qs

class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Parseamos la URL para extraer la ruta y parámetros
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            with open('index.html', 'r', encoding='utf-8') as f:    # archivo del formulario
                html_content = f.read()

            self._send_html_response(html_content)
        else:
            self._send_error_response(404, 'Página no encontrada')
    
    def do_POST(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data_bytes = self.rfile.read(content_length)
            
            post_data = parse_qs(post_data_bytes.decode('utf-8'))
            
            processed_data = {key: value[0] for key, value in post_data.items()}
            
            # Generamos una página de confirmación con los datos recibidos
            confirmation_html = f'''
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Datos Recibidos</title>
            </head>
            <body>
                <h1>Formulario Recibido</h1>
                <p>Datos recibidos:</p>
                <pre>{json.dumps(processed_data, indent=4, ensure_ascii=False)}</pre>
            </body>
            </html>
            '''
            self._send_html_response(confirmation_html)
        else:
            self._send_error_response(404, 'Ruta no encontrada para POST')
    



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