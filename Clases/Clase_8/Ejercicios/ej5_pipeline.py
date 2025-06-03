'''
Objetivo: diseñar un pipeline productor–consumidor usando Pipe doble.

Crea dos procesos hijos: productor genera 10 números pseudo‑aleatorios y los envía al padre;

el padre los reenvía a un consumidor, que imprime el cuadrado de cada número.

Implementa el pipeline con dos Pipe(), asegurando el cierre limpio de extremos y
detectando fin de datos mediante envío del valor None.
'''

from multiprocessing import Process, Pipe
import random


def productor(Productor_conn):
    
    for i in range(10):
        num = random.randint(1, 100)
        print(f"Productor: {num}")
        
        Productor_conn.send(num)
        
    Productor_conn.send(None) # Envío de None para indicar el fin de datos
    
    Productor_conn.close() # Cierra el extremo del pipe
    print("Productor: Fin de la ejecución")


def consumidor(Consumidor_conn):
    
    while True:
        
        num = Consumidor_conn.recv() # Recibe números del padre por el pipe
        
        if num is None: # Al recibir None, rompe el bucle 
            break
    
        print(f"Consumidor: {num}**2 = {num ** 2}")
    
    Consumidor_conn.close() # Cierra el extremo del pipe
    print("Consumidor: Fin de la ejecución")
    

if __name__ == '__main__':
    Productor_conn, Padre_conn_productor = Pipe()
    Consumidor_conn, Padre_conn_consumidor = Pipe()
    
    productor = Process(target=productor, args=(Productor_conn,))    
    consumidor = Process(target=consumidor, args=(Consumidor_conn,))
    
    numeros = []
    
    productor.start()
    for i in range(11):
        num = Padre_conn_productor.recv() # Recibe el número del productor
        numeros.append(num)
    
    consumidor.start()
    for num in numeros:
        Padre_conn_consumidor.send(num) # Envía el número al consumidor
    
    productor.join()
    consumidor.join()
    
    print("Fin del pipeline")