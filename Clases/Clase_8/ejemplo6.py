from multiprocessing import Process
import os, time

def tarea():
    print(f"Hijo empezó")
    time.sleep(10)
    print("Hijo terminando")

if __name__ == "__main__":
    print(f"Padre PID {os.getpid()} crea un hijo")
    p = Process(target=tarea)
    print(p.pid) # devuelve none
    p.start()
    print(p.pid) # devuelve el pid del hijo
    time.sleep(20)  # este ocurre en paralelo con el del hijo, por eso es mas largo para verlo zombie
    p.join()
    time.sleep(10)
    print("Hijo finalizado")