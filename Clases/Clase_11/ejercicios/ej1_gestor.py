## Ejercicio 1: Creación de Procesos con Argumentos
'''
Script `gestor.py` que reciba argumentos de CLI con `argparse`:

- La opción `--num` indica la cantidad de procesos hijos a crear.
- La opción `--verbose` activa mensajes detallados.

Cada proceso hijo debe dormir entre 5 y 10 segundos y luego terminar.

El proceso padre debe imprimir su PID y
mostrar la jerarquía de procesos usando `pstree -p`.

Desde otra terminal, el estudiante deberá observar el
estado de los procesos con `ps` o accediendo a `/proc`.
'''

import argparse
import os
import time
import multiprocessing
import random

def child_process():
    time.sleep(random.randint(5, 10))
    
    if args.verbose:
        print(f"Proceso hijo {os.getpid()} ha terminado.")



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Gestor de procesos")

    parser.add_argument("-n", "--num", required=True, help="Número de procesos hijos", type=int)
    parser.add_argument("-v", "--verbose", action="store_true", help="Activar mensajes detallados")

    args = parser.parse_args()
   

    
    pid_padre = os.getpid()
    
    print(f"PID del padre: {pid_padre}")
    
    processes = []
    
    for i in range(args.num): # crea n procesos hijos
        
        if args.verbose:
            print(f"Creando hijo {i + 1} de {args.num}...")
        
        p = multiprocessing.Process(target=child_process)
        processes.append(p)
        p.start()

    os.system(f"pstree -p {pid_padre}")

    for p in processes:
        p.join()
         
    time.sleep(10) # para poder ver el estado de los procesos hijos con pstree -ef
         
    if args.verbose:
        print("Todos los procesos hijos han terminado.")