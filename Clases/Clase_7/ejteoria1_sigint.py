# Básico: Crear un programa que imprima un mensaje al recibir SIGINT.


import signal
import time
import os

def handler_personalizado(signum, frame):
    
    # Signum es el número de la señal recibida
    # Frame es el marco de pila en el que se recibió la señal
    
    if signum == signal.SIGINT: # Verifica si la señal es SIGINT
        print(os.getpid())
        print("Recibida señal: SIGINT")
        exit(0)
        
# Asociar la señal SIGINT con el handler que creamos, en lugar del default
signal.signal(signal.SIGINT, handler_personalizado)

print("Esperando señales")
print(os.getpid())
while True:
    time.sleep(1)