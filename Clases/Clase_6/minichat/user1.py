'''
VERSION BLOQUEANTE, LA VERSION NO BLOQUEANTE
(donde el que comience a escribir pueda ser cualquiera y no se bloquee innecesariamente)
CONSULTARLA CON EL PROFESOR
'''

import os

fifo_write = "/tmp/chat1to2"  # FIFO para enviar mensaje a user2
fifo_read = "/tmp/chat2to1"   # FIFO para leer mensaje de user2

# Crear los FIFOs si no existen
if not os.path.exists(fifo_write):
    os.mkfifo(fifo_write)
if not os.path.exists(fifo_read):
    os.mkfifo(fifo_read)

# Enviar mensaje
while True:
    fw = os.open(fifo_write, os.O_WRONLY)  # Abrir FIFO en modo escritura (bloqueante)
    msg = input("User 1: ")  # El usuario ingresa un mensaje
    msg = msg + '\n'
    os.write(fw, msg.encode())  # Escribir el mensaje en el FIFO
    os.close(fw)  # Cerrar el FIFO después de escribir

    # Leer respuesta
    fr = os.open(fifo_read, os.O_RDONLY)  # Abrir FIFO en modo lectura (bloqueante)
    respuesta = os.read(fr, 1024).decode().strip()  # Leer del FIFO
    print(f"User 2: {respuesta}")  # Mostrar respuesta
    os.close(fr)  # Cerrar el FIFO después de leer
