import signal
import time
import os

def handler_personalizado(signum, frame):
    
    # Signum es el número de la señal recibida
    # Frame es el marco de pila en el que se recibió la señal
    
    if signum == signal.SIGKILL: # Verifica si la señal es SIGKILL
        print(os.getpid())
        print("Recibida señal: SIGKILL")
        exit(0)
        
# Asociar la señal SIGKILL con el handler que creamos, en lugar del default
signal.signal(signal.SIGKILL, handler_personalizado)

print("Esperando señales")
print(os.getpid())
while True:
    time.sleep(1)
    
# EN ESTE CASO, TIRA ERROR EL KERNEL PORQUE NO ME PERMITE CAPTURAR SIGKILL
# NI MODIFICAR SU HANDLER, ES COMO LA ULTIMA OPCION DEL SISTEMA PARA MATAR
# PROCESOS QUE NO RESPONDEN O TERMINAN