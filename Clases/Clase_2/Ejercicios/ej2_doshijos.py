# Ejercicio 2: Crear dos hijos desde el mismo padre
# Objetivo: ver cómo un solo padre puede lanzar múltiples procesos hijos.

import os

for i in range(2):
    pid = os.fork()
    if pid == 0:
        print(f"Hijo {i}: {os.getpid()} , Padre {os.getppid()}")
        os._exit(0)

for j in range(2):
    os.wait()