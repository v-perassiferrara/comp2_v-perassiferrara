# Programa que use fork y cree un hijo por cada padre, pero cada padre solo puede tener un hijo

import os, time

def crear_hijos():

    for i in range(5): # Crea 5 padres
        pid = os.fork()
        if pid == 0:

            print(f"    Soy el padre {i}: {os.getpid()}")
            pid2 = os.fork() # Crea un padre para cada hijo

            if pid2 == 0:
                print(f"        Soy el hijo de {os.getppid()}")
                # time.sleep(20)
                os._exit(0)
            os.wait()
            os._exit(0)


if __name__ == "__main__":
    crear_hijos()
    os.wait()
    print(f"Soy el abuelo {os.getpid()}")