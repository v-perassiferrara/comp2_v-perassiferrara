import threading
import time

# Definimos nuestros dos locks
lock_A = threading.Lock()
lock_B = threading.Lock()

def funcion_1():
    print("Función 1: Intentando adquirir Lock A...")
    lock_A.acquire() # Adquiere Lock A
    print("Función 1: Lock A adquirido. Esperando un momento...")
    time.sleep(0.1) # Simula algún trabajo
    
    print("Función 1: Intentando adquirir Lock B...")
    lock_B.acquire() # Intenta adquirir Lock B
    print("Función 1: Ambos Locks (A y B) adquiridos.")
    
    # Realiza operaciones con ambos recursos
    print("Función 1: Realizando operaciones críticas...")
    time.sleep(0.1)
    
    lock_B.release()
    lock_A.release()
    print("Función 1: Locks (B y A) liberados.")

def funcion_2():
    print("Función 2: Intentando adquirir Lock B...")
    lock_B.acquire() # Adquiere Lock B
    print("Función 2: Lock B adquirido. Esperando un momento...")
    time.sleep(0.1) # Simula algún trabajo
    
    print("Función 2: Intentando adquirir Lock A...")
    lock_A.acquire() # Intenta adquirir Lock A
    print("Función 2: Ambos Locks (B y A) adquiridos.")
    
    # Realiza operaciones con ambos recursos
    print("Función 2: Realizando operaciones críticas...")
    time.sleep(0.1)
    
    lock_A.release()
    lock_B.release()
    print("Función 2: Locks (A y B) liberados.")

print("Iniciando simulación de deadlock...")

# Creamos los hilos
hilo1 = threading.Thread(target=funcion_1)
hilo2 = threading.Thread(target=funcion_2)

# Iniciamos los hilos
hilo1.start()
hilo2.start()

# Esperamos a que los hilos terminen (aunque en caso de deadlock, nunca terminarán)
hilo1.join()
hilo2.join()

print("Simulación terminada.")