# Ejercicio 7: Crear múltiples procesos simultáneos
# Objetivo: observar la expansión del árbol de procesos.

import os, time

print("PID del proceso padre:", os.getpid())

for i in range(4):
    pid = os.fork()
    if pid == 0:
        print(f"Hijo {i}: {os.getpid()} , Padre {os.getppid()}")
        time.sleep(10)
        os._exit(0)  # Si se comenta, los hijos siguen el bucle y se producen más procesos

time.sleep(20) # padre espera para que no desaparezca/finalice