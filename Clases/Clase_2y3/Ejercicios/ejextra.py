# Programa que use fork y cree dos hijos, cada uno con un sleep distinto, donde cada uno diga "Soy un hijo, mi PID es ..."
# Que el padre no haga wait y al final escriba "Soy el padre"

import os, time

def crear_hijo(tiempo_espera, mensaje):
    pid = os.fork()
    if pid == 0:
        time.sleep(tiempo_espera)
        print(f"{mensaje}, mi PID es: {os.getpid()}")
        os._exit(0)

if __name__ == "__main__":
    crear_hijo(2,"Hijo 1")
    crear_hijo(3,"Hijo 2")

    # time.sleep(1)
    os.wait()
    os.wait()
    print(f"Soy el padre {os.getpid()}")