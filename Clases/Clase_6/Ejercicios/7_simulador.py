'''
Ejercicio 7 — Monitor de temperatura simulado
Objetivo: Simular un sensor que envía datos por FIFO y un visualizador que los muestra.

Instrucciones:

Script A (simulador): cada segundo escribe en el FIFO una temperatura aleatoria entre 20 y 30.
Script B (monitor): lee las temperaturas y muestra alertas si superan los 28 grados.
Variante: Agregar un log con fecha y hora.
'''

import os, time, random
from datetime import datetime

fifo = "/tmp/fifo_temperatura"
# Asegurarse de que exista
try:
    os.mkfifo(fifo)
except FileExistsError:
    pass

num_temperaturas = 50

print("Abriendo FIFO para enviar temperaturas...")
with open(fifo, 'w') as f:
    while num_temperaturas > 0:
        msg = str(random.uniform(20, 30))   # Genera un número float aleatorio entre 20 y 30
        msg = '[' + datetime.now().strftime("%H:%M:%S") + '] ' + msg + '\n'
        f.write(msg)
        f.flush()
        print(f"Enviado: {msg.strip()}")
        num_temperaturas -= 1
        time.sleep(1)
    
