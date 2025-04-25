'''
Ejercicio 4 — Múltiples productores
Objetivo: Estudiar el comportamiento de múltiples escritores sobre un mismo FIFO.

Instrucciones:

Crear un FIFO /tmp/fifo_multi.
Ejecutar tres scripts distintos que escriban mensajes periódicamente (por ejemplo, "Soy productor 1", etc.).
Un solo lector debe mostrar los mensajes.

Reflexión:
¿Se mezclan las líneas?
No. Cada línea completa se escribe de forma atómica mientras sea corta (≤ PIPE_BUF), así que no se mezclan contenidos entre procesos.

¿Qué pasa si escriben al mismo tiempo?
Las líneas pueden intercalarse en el orden, pero no se corrompen. Esto es porque
es un sistema no determinista. El FIFO no garantiza el orden de llegada de los mensajes,
pero sí garantiza que cada línea se escriba completa (si no se supera PIPE_BUF).

¿Es atómico?
Sí, mientras el mensaje no supere PIPE_BUF. Si lo supera, podría mezclarse con otros.
'''

import os

fifo = '/tmp/fifo_multi'
# Asegurarse de que exista
try:
    os.mkfifo(fifo)
except FileExistsError:
    pass

while True:
    with open('/tmp/fifo_multi', 'r') as fifo:
        for line in fifo:
            print(f"Recibido: {line.strip()}")