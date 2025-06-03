from multiprocessing import Process, Lock, Value
import time

def sumar(variable, lock, i):
    print(f"Proceso {i}: Intentando adquirir lock para incremento...")
    with lock:
        print(f"Proceso {i}: Lock adquirido para incremento.")
        for _ in range(1000):
            variable.value += 1
        print(f"Proceso {i}: Incremento completado.")
        
        print(f"Proceso {i}: Llamando a multiplicar()...")
        multiplicar(variable, lock, i)

def restar(variable, lock, i):
    print(f"Proceso {i}: Intentando adquirir lock para resta...")
    with lock:
        print(f"Proceso {i}: Lock adquirido para resta.")
        variable.value -= 10
        print(f"Proceso {i}: Resta completada.")
        
        print(f"Proceso {i}: Llamando a multiplicar()...")
        multiplicar(variable, lock, i)

def multiplicar(variable, lock, i):
    print(f"Proceso {i}: Intentando adquirir lock para multiplicación...")
    with lock:
        print(f"Proceso {i}: Lock adquirido para multiplicación.")
        for _ in range(5):
            variable.value *= 2
        print(f"Proceso {i}: Multiplicación completada.")

if __name__ == '__main__':
    contador = Value('i', 0)  # Contador entero compartido
    lock = Lock()           # Lock para permitir reentrancia

    p1 = Process(target=sumar, args=(contador, lock, 1))
    p2 = Process(target=restar, args=(contador, lock, 2))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print(f"Valor final del contador: {contador.value}")