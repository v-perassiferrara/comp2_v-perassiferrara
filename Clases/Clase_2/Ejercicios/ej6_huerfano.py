# Ejercicio 6: Crear un proceso huérfano
# Objetivo: observar la adopción de procesos por init.

import os, time

pid = os.fork()

if pid == 0:
    print(f"Hijo: {os.getpid()} es ahora huerfano. Nuevo padre {os.getppid()}") # el hijo perdio a su padre, por lo que es adoptado por systemd/init
    time.sleep(5)

else:
    print(f"Padre: {os.getpid()}. Finalizando")
    os._exit(0) # padre finaliza mientras hijo sigue