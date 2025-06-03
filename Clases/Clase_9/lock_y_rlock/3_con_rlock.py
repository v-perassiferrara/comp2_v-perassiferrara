from multiprocessing import Process, RLock, Value
import time

def sumar(variable, rlock, i):
    print(f"Proceso {i}: Intentando adquirir lock para incremento...")
    with rlock:
        print(f"Proceso {i}: Lock adquirido para incremento.")
        for _ in range(1000):
            variable.value += 1
        print(f"Proceso {i}: Incremento completado.")
        
        print(f"Proceso {i}: Llamando a multiplicar()...")
        multiplicar(variable, rlock, i)

def restar(variable, rlock, i):
    print(f"Proceso {i}: Intentando adquirir lock para resta...")
    with rlock:
        print(f"Proceso {i}: Lock adquirido para resta.")
        variable.value -= 10
        print(f"Proceso {i}: Resta completada.")
        
        print(f"Proceso {i}: Llamando a multiplicar()...")
        multiplicar(variable, rlock, i)

def multiplicar(variable, rlock, i):
    print(f"Proceso {i}: Intentando adquirir lock para multiplicación...")
    with rlock:
        print(f"Proceso {i}: Lock adquirido para multiplicación.")
        for _ in range(5):
            variable.value *= 2
        print(f"Proceso {i}: Multiplicación completada.")

if __name__ == '__main__':
    contador = Value('i', 0)  # Contador entero compartido
    rlock = RLock()           # RLock para permitir reentrancia

    p1 = Process(target=sumar, args=(contador, rlock, 1))
    p2 = Process(target=restar, args=(contador, rlock, 2))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print(f"Valor final del contador: {contador.value}")