
'''
Ejercicio 1: Manejo básico con SIGTERM
Objetivo: Familiarizarse con el uso de SIGTERM y funciones de limpieza al finalizar un proceso.

Enunciado: Crea un programa que capture la señal SIGTERM y responda con un mensaje de despedida.
Asegúrate de registrar una función con atexit para que se ejecute al terminar el proceso,
independientemente del motivo de finalización.
'''

import signal, time, atexit, os, sys

def final():
    print("Programa terminado")

# Definir una función manejadora para señales
def handler(signum, frame):
    # Imprimir un mensaje indicando que se ha recibido una señal
    print(f"Recibida señal: {signum}")
    sys.exit(0)

atexit.register(final)

# Asociar la señal SIGTERM con la función manejadora 'handler'
signal.signal(signal.SIGTERM, handler)

# Imprimir un mensaje indicando que el programa está esperando señales
print("Esperando señales")

# Mantener el programa en ejecución para que pueda recibir señales
while True:
# Pausar la ejecución durante 1 segundo para reducir el uso de CPU
    print(os.getpid())
    time.sleep(1)
