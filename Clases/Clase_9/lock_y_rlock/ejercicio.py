'''
Log Concurrente
Escribe un programa donde 5 procesos intentan escribir mensajes en un único archivo de log (`log.txt`).
Cada mensaje debe incluir el ID del proceso y una marca de tiempo.
Usa un `Lock` para asegurar que las líneas de log no se mezclen y cada escritura sea completa.
'''

from multiprocessing import Process, Lock
from datetime import datetime
import os


def escribir(lock):
    
    with lock:
        
        with open('log.txt', 'a') as log:    
               
            log.write(f"Proceso {os.getpid()} escribió. | {datetime.now()}\n") 

        


def main():
    lock = Lock()
    procesos = []
    
    for i in range(5):
        p = Process(target=escribir, args=(lock,))
        procesos.append(p)
        p.start()
    
    for p in procesos:
        p.join()
        
        

if __name__ == '__main__':
    main()
    with open('log.txt', 'r') as log: 
        print(log.read())