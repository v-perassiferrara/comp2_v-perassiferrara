'''
1) Múltiples Productores y un Consumidor:
    Modifica el ejemplo para que haya dos o más procesos productores enviando mensajes a una sola cola que es procesada por un único consumidor.
'''

'''

Esta versión si funciona. Lo que plantea la IA es utilizar managar.Queue() en lugar de multiprocessing.Queue().

Si aún querés mantener Queue, la solución más estable con fork puro es:

✅ Usar una implementación basada en multiprocessing.Manager().Queue(), que no tiene procesos internos.
Este tipo de cola es menos eficiente, pero 100% compatible con os.fork(), porque no necesita subprocessos propios. Así que no se cuelga.

'''


import os
import time
from multiprocessing import Manager

def productor(q, i):
    print(f"Productor {i} para escribir...")
    for j in range(5):
        msg = f"Mensaje {j} de productor {i}"
        q.put(msg)
        print(f"Productor {i} envió: {msg}")
        time.sleep(0.5)
    q.put("FIN")
    os._exit(0)

def consumidor(q, num_productores):
    print("Consumidor esperando mensaje...")
    num_fines = 0
    while True:
        msg = q.get()
        if msg == "FIN":
            num_fines += 1
            if num_fines == num_productores:
                break
        else:
            print(f"Consumidor recibió: {msg}")
            time.sleep(0.5)
    print("Consumidor terminando.")
    os._exit(0)

def main():
    with Manager() as manager:
        q = manager.Queue()
        num_productores = 2

        # Crear productores
        for i in range(num_productores):
            pid = os.fork()
            if pid == 0:
                productor(q, i)

        # Crear consumidor
        pid = os.fork()
        if pid == 0:
            consumidor(q, num_productores)

        # Esperar todos los hijos
        for _ in range(num_productores + 1):
            os.wait()

        print("Fin de la comunicación.")

if __name__ == "__main__":
    main()
