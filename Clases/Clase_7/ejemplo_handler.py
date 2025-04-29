import signal
import time

import signal
import time

# Definir una función manejadora para señales
def handler(signum, frame):
    # Imprimir un mensaje indicando que se ha recibido una señal
    print(f"Recibida señal: {signum}")

# Asociar la señal SIGUSR1 con la función manejadora 'handler'
signal.signal(signal.SIGUSR1, handler)

# Imprimir un mensaje indicando que el programa está esperando señales
print("Esperando señales")

# Mantener el programa en ejecución para que pueda recibir señales
while True:
    # Pausar la ejecución durante 1 segundo para reducir el uso de CPU
    time.sleep(1)
    
    
# Esto genera:
#
# Esperando señales
# Recibida señal: 10