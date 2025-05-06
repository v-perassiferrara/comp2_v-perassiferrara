from multiprocessing import Process
import os, time

def tarea():
    print(f"Hijo PID {os.getpid()}")
    time.sleep(10)
    print("Hijo terminando")

if __name__ == "__main__":
    print(f"Padre PID {os.getpid()} crea un hijo")
    p = Process(target=tarea)
    time.sleep(10)
    p.start()
    time.sleep(20)  # este ocurre en paralelo con el del hijo, por eso es mas largo para verlo zombie
    p.join()
    print("Hijo finalizado")
    
# hacer pstree -p [id padre]
# por ejemplo: pstree -p 33644   genera   python(33644)───python(33719)

# el fork sucede recién en el start 

# para ver al hijo zombie usar ps