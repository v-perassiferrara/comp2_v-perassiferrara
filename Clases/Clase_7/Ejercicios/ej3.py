
'''
Ejercicio 3: Ignorar señales temporalmente
Objetivo: Controlar cuándo un programa debe responder a una señal.r

Enunciado: Crea un programa que ignore SIGINT (Ctrl+C) durante los primeros 5 segundos de ejecución.
Luego, el programa debe restaurar el comportamiento por defecto para esa señal y
continuar ejecutando indefinidamente. Verifica que Ctrl+C no interrumpe el programa durante
los primeros segundos, pero sí lo hace después.
'''

import signal
import time
import os

signal.signal(signal.SIGINT, signal.SIG_IGN) # Ignorar la señal SIGINT

time.sleep(5)  # Esperar primeros 5 segundos

signal.signal(signal.SIGINT, signal.SIG_DFL) # Restaurar el comportamiento por defecto para SIGINT


print("Esperando señales")
print(os.getpid())
while True:
    time.sleep(1)
