# Avanzado: Crear un programa multihilo donde un hilo central
# recibe señales con sigwait() y despacha tareas.


import signal
import time

def handler(signum, frame):
    if signum == signal.SIGINT:
        print("Recibida señal: SIGINT")
        exit(0)
signal.signal(signal.SIGINT, handler)
print("Esperando señales")
while True:
    time.sleep(1)