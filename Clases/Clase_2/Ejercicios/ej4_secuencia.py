# Ejercicio 4: Crear procesos secuenciales
# Objetivo: lanzar un hijo, esperar su finalización, y luego crear otro.


import os, time

for i in range(2):
    pid = os.fork()
    
    if pid == 0:
        print(f"Hijo: {os.getpid()}, Padre: {os.getppid()}")
        time.sleep(3)
        os._exit(0)
    else:
        os.wait()