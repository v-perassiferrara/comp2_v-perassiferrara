'''
Ejercicio 5: Calculadora Remota

Objetivo: Implementar una calculadora cliente-servidor con IPv6.

Requisitos del servidor:

    Recibir expresiones matemáticas
    Evaluar la expresión de forma segura
    Devolver el resultado
    Manejar errores apropiadamente

Requisitos del cliente:

    Interfaz simple para ingresar expresiones
    Mostrar resultados
    Manejar errores de conexión


Ejemplo:

Cliente: "2 + 2"
Servidor: "RESULTADO: 4"

Cliente: "10 / 0"
Servidor: "ERROR: División por cero"

'''

import socketserver
import socket

class HandlerCalculadora(socketserver.BaseRequestHandler):
    def handle(self):
        
        # Recibir datos
        data = self.request.recv(1024).strip()
        print(f"Recibido: {data.decode()}")
        
        valores = data.split(b" ")
        
        if len(valores) != 3:   # solo admitimos operaciones de dos operandos (a + b, a - b, etc.)
            self.request.sendall("ERROR: Formato de expresión incorrecto. Usa 'a + b', 'a - b', etc.\n".encode())
            return
        
        operando1 = int(valores[0])
        operando2 = int(valores[2])
        
        operador = valores[1].decode()
        
        
        # Evaluar expresión
        if operador == "+":
            resultado = operando1 + operando2
        elif operador == "-":
            resultado = operando1 - operando2
        elif operador == "*":
            resultado = operando1 * operando2
        elif operador == "/":
            resultado = operando1 / operando2
        else:
            self.request.sendall(f"ERROR: Operador no reconocido: {operador}\n".encode())
            return
        
        # Enviar respuesta
        respuesta = f"Resultado: {resultado}\n"
        self.request.sendall(respuesta.encode())

# Crear clase de servidor IPv6
class ServidorIPv6(socketserver.TCPServer):
    address_family = socket.AF_INET6    # usamos socket de IPv6
    allow_reuse_address = True  # permite reusar la direccion

if __name__ == "__main__":
    HOST, PORT = "::1", 9990
    
    with ServidorIPv6((HOST, PORT), HandlerCalculadora) as servidor:
        print(f"Servidor IPv6 iniciado en [{HOST}]:{PORT}")
        servidor.serve_forever()