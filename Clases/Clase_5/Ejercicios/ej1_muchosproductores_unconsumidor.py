'''
1) Múltiples Productores y un Consumidor:
    Modifica el ejemplo para que haya dos o más procesos productores enviando mensajes a una sola cola que es procesada por un único consumidor.
'''

import os
import time
from multiprocessing import Queue

def productor(q):
    print("Padre esperando a para escribir")
    
    for i in range(5):
        msg = f"Mensaje {i}"
        q.put(msg)
        
        print(f"Padre envió: {msg}")
        
        time.sleep(0.5)
    
    q.put("FIN")

def consumidor(q):
    print("Hijo esperando mensaje...")
    while True:
        
        mensaje = q.get(timeout=5)  # Lanza excepción si pasan 5 segundos para evitar deadlock
        
        if mensaje == "FIN":
            break
        
        print(f"Hijo recibió: {mensaje}")
        
        time.sleep(0.5)
    
    print("Hijo: terminando.")

def main():
    q = Queue(10) # El argumento especifica una capacidad máxima de 10 elementos
    
    pid = os.fork()
    
    if pid == 0:
        # Proceso hijo: consumidor
        consumidor(q)
        os._exit(0)
    else:
        # Proceso padre: productor
        productor(q)
        os.wait()  # Espera a que el proceso hijo termine
        print("Padre: fin de la comunicación.")

if __name__ == "__main__":
    main()
