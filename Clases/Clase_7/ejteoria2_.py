# Intermedio: Registrar múltiples señales con sigaction()
# y proteger secciones críticas con sigprocmask().


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