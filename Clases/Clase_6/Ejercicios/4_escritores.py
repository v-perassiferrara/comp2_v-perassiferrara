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

import os, time

fifo = '/tmp/fifo_multi'
# Asegurarse de que exista
try:
    os.mkfifo(fifo)
except FileExistsError:
    pass

numero_escritores = 3

numero_mensajes = 5


for i in range(numero_escritores):
    pid = os.fork()

    if pid == 0:  # Código del hijo
        for j in range(numero_mensajes):
            with open(fifo, 'w') as f:
                msg = f"Escritor {i+1} - Msg {j+1}\n" 
                f.write(msg)
                print(f"Enviado: {msg.strip()}")
            time.sleep(0.1)
        os._exit(0)

for _ in range(numero_escritores):
    os.wait()  # Espera a que terminen todos los procesos hijos