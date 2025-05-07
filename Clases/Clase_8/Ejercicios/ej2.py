'''
Ejercicio 2 · Nivel Intermedio
Objetivo: usar Queue para reunir resultados de varios procesos.

Implementa un script que genere n = 4 procesos;
cada proceso calcula la suma de los primeros 
k = 1.000.000 enteros y deposita el resultado en una Queue.

El padre recoge los cuatro resultados y verifica que sean idénticos.
'''

from multiprocessing import Process, Queue

n = 4 # número de procesos

k = 1000000 # número de enteros a calcular

def calcular_suma(k, q):
    suma = sum(range(k))
    q.put(suma) # depositar el resultado en la Queue

q = Queue()
resultados = []
procesos = []

for i in range(n):
    p = Process(target=calcular_suma, args=(k, q))
    p.start()
    procesos.append(p)

for p in procesos:
    p.join()

for i in range(n):
    resultados.append(q.get())

for i in range(n):
    if resultados[i] != resultados[0]:
        print(f"Error: el resultado del proceso {i} es diferente.")
        break
    print(f"El resultado del proceso {i} es correcto: {resultados[i]}")
print("Todos los resultados son correctos.")