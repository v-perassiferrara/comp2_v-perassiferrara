'''
Ejercicio 7 — Monitor de temperatura simulado
Objetivo: Simular un sensor que envía datos por FIFO y un visualizador que los muestra.

Instrucciones:

Script A (simulador): cada segundo escribe en el FIFO una temperatura aleatoria entre 20 y 30.
Script B (monitor): lee las temperaturas y muestra alertas si superan los 28 grados.
Variante: Agregar un log con fecha y hora.
'''

import os

fifo = "/tmp/fifo_temperatura"
# Asegurarse de que exista
try:
    os.mkfifo(fifo)
except FileExistsError:
    pass

max_temperatura = 28

print("Abriendo FIFO para recibir...")

with open(fifo, 'r') as f:
    
    for linea in iter(f.readline, ''):
        if float(linea.strip().split()[1]) > max_temperatura:
            print(f"[ALERTA: Alta Temperatura]: {linea.strip()}")
            continue
        print(f"Recibido: {linea.strip()}")

