'''
Ejercicio 2: Diferenciar señales según su origen
Objetivo: Comprender cómo múltiples señales pueden ser diferenciadas en un mismo handler.

Enunciado: El proceso principal debe lanzar tres procesos hijos.
Cada hijo, luego de un pequeño retardo aleatorio,
debe enviar una señal distinta al padre (SIGUSR1, SIGUSR2, SIGTERM).
El padre debe manejar todas las señales con un solo handler y registrar cuál hijo envió qué señal,
usando os.getpid() y os.getppid().
'''

import signal
import time
import os
import sys
import random

# Handler único
def handler_personalizado(signum, frame):
    if signum == signal.SIGUSR1:
        print("Recibido SIGUSR1 del hijo 1")
    elif signum == signal.SIGUSR2:
        print("Recibido SIGUSR2 del hijo 2")
    elif signum == signal.SIGTERM:
        print("Recibido SIGTERM del hijo 3")

# Asociar las señales al handler
signal.signal(signal.SIGUSR1, handler_personalizado)
signal.signal(signal.SIGUSR2, handler_personalizado)
signal.signal(signal.SIGTERM, handler_personalizado)

print("Esperando señales")
print("Padre:", os.getpid())

# Lista de señales para cada hijo
señales = [signal.SIGUSR1, signal.SIGUSR2, signal.SIGTERM]
pids_hijos = []

for i in range(3):
    pid = os.fork()

    if pid == 0:  # Hijo
        time.sleep(1)
        print(f"Hijo {i+1} (PID {os.getpid()}) envía señal {señales[i]}")
        os.kill(os.getppid(), señales[i])
        os._exit(0)  # Finaliza sin ejecutar más código

    else:
        pids_hijos.append(pid)

# Padre: espera a que terminen los 3 hijos
for _ in range(3):
    os.wait()

print("Fin del programa padre.")