'''
Ejercicio 1 · Nivel Básico
Objetivo: comprobar la creación de procesos y la correcta espera del padre.

Enunciado: escribe un programa que cree dos procesos hijo mediante multiprocessing.Process,
cada uno imprimiendo su propio pid.
El proceso padre debe esperar a que ambos terminen y luego imprimir un mensaje de cierre.
'''

from multiprocessing import Process
import os

def hijo():
    print(f"Soy el proceso hijo con PID: {os.getpid()}")
    
hijo1 = Process(target=hijo)
hijo2 = Process(target=hijo)

hijo1.start()
hijo2.start()

hijo1.join()
hijo2.join()

print(f"Fin del padre {os.getpid()}")