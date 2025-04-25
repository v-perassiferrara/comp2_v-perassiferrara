'''
Ejercicio 2 — FIFO como buffer entre procesos
Objetivo: Simular un flujo de datos continuo entre dos procesos.

Instrucciones:

Crear un proceso productor que escriba números del 1 al 100 en el FIFO con un sleep(0.1).
Crear un consumidor que lea esos números del FIFO y los imprima con su timestamp local.
Asegurarse de que ambos scripts se ejecuten en paralelo.

Extensión: Agregar lógica en el consumidor para detectar si falta un número (por ejemplo, si no es consecutivo).
    
'''

from datetime import datetime

fifo = 'fifo_prueba2'

print("Abriendo FIFO para lectura…")

ultimo_numero = None

with open(fifo, 'r') as f:
    for linea in f:
        timestamp = datetime.now()
        numero = int(linea.strip().split()[1])
        
        
        if ultimo_numero is not None and numero != ultimo_numero + 1:
            print(f"Falta el número: {ultimo_numero + 1}")
           
        
        print(f"Recibido: {timestamp} | {linea.strip()}")
        
        ultimo_numero = numero