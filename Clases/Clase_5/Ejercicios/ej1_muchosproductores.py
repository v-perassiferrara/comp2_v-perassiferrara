'''
1) Múltiples Productores y un Consumidor:
    Modifica el ejemplo para que haya dos o más procesos productores enviando mensajes a una sola cola que es procesada por un único consumidor.
'''

'''
Este codigo no funciona (no termina correctamente), la explicación de la IA es:

❗ Problema real: incompatibilidad parcial
multiprocessing.Queue fue diseñada para funcionar con multiprocessing.Process, no con os.fork() puro.
Cuando forkeás un proceso, la cola es copiada, y sus mecanismos internos de cierre y sincronización no detectan correctamente cuándo todos los procesos hijos terminaron.

Esto hace que:
    - El proceso principal se quede colgado en os.wait() o incluso en operaciones internas de la cola.
    - Aunque FIN se reciba, los procesos pueden quedar vivos por colas no cerradas del todo.

'''


import os
import time
from multiprocessing import Queue

def productor(q,i):
    print(f"Productor {i} para escribir...")
    
    for j in range(5):
        msg = f"Mensaje {j} de productor {i}"
        q.put(msg)
        
        print(f"Productor {i} envió: {msg}")
        
        time.sleep(0.5)
    
    q.put("FIN")

def consumidor(q,num_productores):
    print("Consumidor esperando mensaje...")
    
    num_fines = 0
    
    while True:
        
        mensaje = q.get(timeout=5)  # Lanza excepción si pasan 5 segundos para evitar deadlock
        
        if mensaje == "FIN":
            num_fines += 1
            if num_fines == num_productores:
                break
        
        print(f"Consumidor recibió: {mensaje}")
        
        time.sleep(0.5)
    
    print("Consumidor terminando.")

def main():
    q = Queue(20) # El argumento especifica una capacidad máxima de 10 elementos
    
    num_productores = 2
    
    # Crear productores
    for i in range(num_productores):
        pid = os.fork()
        if pid == 0:
            # Productor
            productor(q,i)
            os._exit(0)
    
    
    # Crear consumidor
    pid = os.fork()
    if pid == 0:
        # Consumidor
        consumidor(q,num_productores)
        os._exit(0)

    for i in range(num_productores + 1):
        os.wait()  # Espera a que los hijos terminen
    
    print("Fin de la comunicación.")

if __name__ == "__main__":
    main()
