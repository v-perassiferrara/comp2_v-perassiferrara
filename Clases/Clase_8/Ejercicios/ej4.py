'''
Ejercicio 4 · Nivel Avanzado
Objetivo: medir el impacto del GIL versus multiprocessing en tareas CPU-bound (intensivas en CPU). 

Implementa la función fibonacci(n) de forma recursiva e imprímela para n = 35
Mide primero el tiempo usando hilos (threading.Thread) con 4 hilos y luego con 4 procesos (multiprocessing.Process)
Compara y explica la diferencia.
'''


# Guía de solución: se espera que la versión con hilos no supere la ejecución secuencial debido al GIL,
# mientras que la versión con procesos reduzca casi 4 × el tiempo.
# Se deben usar time.perf_counter() y presentar los números.


