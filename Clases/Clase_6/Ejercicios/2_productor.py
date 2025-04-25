'''
Ejercicio 2 — FIFO como buffer entre procesos
Objetivo: Simular un flujo de datos continuo entre dos procesos.

Instrucciones:

Crear un proceso productor que escriba números del 1 al 100 en el FIFO con un sleep(0.1).
Crear un consumidor que lea esos números del FIFO y los imprima con su timestamp local.
Asegurarse de que ambos scripts se ejecuten en paralelo.

Extensión: Agregar lógica en el consumidor para detectar si falta un número (por ejemplo, si no es consecutivo).
    
'''

import os, time

fifo = 'fifo_prueba2'
# Asegurarse de que exista
try:
    os.mkfifo(fifo)
except FileExistsError:
    pass

print("Abriendo FIFO para escritura…")
with open(fifo, 'w') as f:
    for i in range(100):
        msg = f"Producto {i+1}\n"
        f.write(msg)
        f.flush()
        print(f"Enviado: {msg.strip()}")
        time.sleep(0.1)