'''
2) Consumidores Concurrentes:
    Implementa varios consumidores que tomen mensajes de la misma cola. Analiza el orden de procesamiento y asegúrate de evitar condiciones de carrera.
'''

import os
import time
from multiprocessing import Queue

def productor(q):
    print("Productor para escribir...")
    
    for i in range(5):
        msg = f"Mensaje {i}"
        q.put(msg)
        
        print(f"Productor envió: {msg}")
        
        time.sleep(0.5)
    
    q.put("FIN")

def consumidor(q,i):
    print(f"Consumidor {i} esperando mensaje...")
    while True:
        
        mensaje = q.get(timeout=5)  # Lanza excepción si pasan 5 segundos para evitar deadlock
        
        if mensaje == "FIN":
            break
        
        print(f"Consumidor {i} recibió: {mensaje}")
        
        time.sleep(0.5)
    
    print(f"Consumidor {i}: terminando.")

def main():
    q = Queue(20) # El argumento especifica una capacidad máxima de 20 elementos
    
    num_consumidores = 2
    
    # Crear productor
    pid = os.fork()
    if pid == 0:
        # Productor
        productor(q)
        os._exit(0)
    
    # Crear consumidores
    for i in range(num_consumidores):
        pid = os.fork()
        if pid == 0:
            # Consumidor
            consumidor(q,i)
            os._exit(0)

    for i in range(num_consumidores + 1):
        os.wait()  # Espera a que los hijos terminen
    
    print("Fin de la comunicación.")

if __name__ == "__main__":
    main()

