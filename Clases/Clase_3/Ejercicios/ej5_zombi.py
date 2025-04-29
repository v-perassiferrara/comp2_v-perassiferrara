# Ejercicio 5: Producir y observar un proceso zombi
# Objetivo: generar un proceso zombi temporal para su inspección.

import os, time

pid = os.fork()

if pid == 0:
    print(f"Hijo {os.getpid()} , Padre {os.getppid()}")
    os._exit(0)

else:
    print("Padre {os,getpid()} esperando al hijo")
    time.sleep(15)