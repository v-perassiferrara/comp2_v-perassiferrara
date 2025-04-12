'''
Ejercicio 6: Servidor de Operaciones Matemáticas
Crea un "servidor" de operaciones matemáticas usando pipes.
El proceso cliente envía operaciones matemáticas como cadenas (por ejemplo, "5 + 3", "10 * 2"),
y el servidor las evalúa y devuelve el resultado.
Implementa manejo de errores para operaciones inválidas.
'''

# Empezó como mi versión y luego la mejoré con ayuda de IA y comparando con la del apunte


import os

def server_math(operando1, operando2, operacion):
    try:
        op1 = float(operando1)
        op2 = float(operando2)
        
        if operacion == "+":
            return op1 + op2
        elif operacion == "-":
            return op1 - op2
        elif operacion == "*":
            return op1 * op2
        elif operacion == "/":
            if op2 == 0:
                raise ZeroDivisionError("División por cero")
            return op1 / op2
        else:
            raise ValueError(f"Operación no soportada: {operacion}")
    
    except ValueError:
        raise ValueError(f"Operación no soportada: {operacion}")

def main():
    r1, w1 = os.pipe()  # Cliente → Server (operaciones)
    r2, w2 = os.pipe()  # Server → Cliente (resultados)

    pid = os.fork()
    
    if pid == 0:  # Cliente
        os.close(r1)
        os.close(w2)
        
        try:
            while True:
                # Enviar operación
                with os.fdopen(w1, 'w') as writer:
                    operation = input("Operación (ej: 5 + 3) o 'exit': ")
                    if operation.lower() == 'exit':
                        writer.write("exit\n")
                        break
                    writer.write(operation + "\n")
                    writer.flush()
                
                # Recibir respuesta
                with os.fdopen(r2) as reader:
                    response = reader.readline().strip()
                    print("Resultado:", response)
        
        finally:
            os._exit(0)
    
    else:  # Servidor
        os.close(w1)
        os.close(r2)
        
        with os.fdopen(r1) as reader, os.fdopen(w2, 'w') as writer:
            while True:
                operation = reader.readline().strip()
                if not operation or operation == "exit":
                    break
                
                try:
                    # Validar formato
                    if operation.count(' ') != 2:   # Si el número de espacios no es 2, da error porque el formato está mal
                        raise ValueError("Formato inválido. Usar: 'num op num'")
                    
                    op1, oper, op2 = operation.split()
                    result = server_math(op1, op2, oper)
                    writer.write(f"{result}\n")
                
                except Exception as e:
                    writer.write(f"Error: {e}\n")
                
                writer.flush()
        
        os.wait()

if __name__ == '__main__':
    main()
