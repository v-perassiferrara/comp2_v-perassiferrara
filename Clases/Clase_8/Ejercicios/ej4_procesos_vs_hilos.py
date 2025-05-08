'''
Ejercicio 4 · Nivel Avanzado
Objetivo: medir el impacto del GIL versus multiprocessing en tareas CPU-bound (intensivas en CPU). 

Implementa la función fibonacci(n) de forma recursiva e imprímela para n = 35

Mide primero el tiempo usando hilos (threading.Thread) con 4 hilos y luego con 4 procesos (multiprocessing.Process)

Compara y explica la diferencia.

'''




'''
Explicación IA sobre time.perf_counter():

perf_counter() es la función recomendada para medir intervalos de tiempo con alta resolución.


# Ejemplo de uso:

t0 = time.perf_counter()
# … ejecución de la tarea …

t1 = time.perf_counter()
print(f"Tiempo transcurrido: {t1 - t0} segundos")

'''




# Resolución por IA ya que no hemos visto threading todavía, aunque en la práctica parece muy similar a multiprocessing

from multiprocessing import Process
import time
import threading

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)  


# Versión secuencial
t0 = time.perf_counter()

for _ in range(4):
    fibonacci(35)

t1 = time.perf_counter()
print(f"Tiempo secuencial: {t1 - t0:.2f} segundos")



# Con procesos
t0 = time.perf_counter()

processes = []

for _ in range(4):
    process = Process(target=fibonacci, args=(35,))
    processes.append(process)
    process.start()
    
    
for process in processes:
    process.join()
    
t1 = time.perf_counter()

print(f"Tiempo con procesos: {t1 - t0:.2f} segundos")



# Con hilos
t0 = time.perf_counter()

threads = []

for _ in range(4):
    thread = threading.Thread(target=fibonacci, args=(35,))
    threads.append(thread)
    thread.start()
    
    
for thread in threads:
    thread.join()
    
t1 = time.perf_counter()

print(f"Tiempo con hilos: {t1 - t0:.2f} segundos")



# Se puede ver que el tiempo con hilos es muy similar al secuencial,
# ya que el GIL no permite que hilos se ejecuten simultáneamente en múltiples núcleos.

# La versión con procesos es mucho más rápida,
# ya que cada proceso tiene su propio GIL y
# puede ejecutarse en un núcleo diferente.