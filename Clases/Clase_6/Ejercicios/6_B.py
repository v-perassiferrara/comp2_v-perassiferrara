'''
Ejercicio 6 — Chat asincrónico con doble FIFO
Objetivo: Crear una estructura de comunicación bidireccional entre dos usuarios.

Instrucciones:

Crear dos FIFOs: /tmp/chat_a y /tmp/chat_b.
Usuario A escribe en chat_a y lee de chat_b, y viceversa.
Implementar dos scripts simétricos, uno para cada usuario.
Extras:

Permitir comandos como /exit para salir.
Mostrar los mensajes con nombre de emisor y timestamp.
'''


import os
from datetime import datetime

fifo_write = "/tmp/chat_b"  # FIFO para enviar mensaje a user1
fifo_read = "/tmp/chat_a"   # FIFO para leer mensaje de user1

# Crear los FIFOs si no existen
if not os.path.exists(fifo_write):
    os.mkfifo(fifo_write)
if not os.path.exists(fifo_read):
    os.mkfifo(fifo_read)

# Leer mensaje
while True:
    fr = os.open(fifo_read, os.O_RDONLY)  # Abrir FIFO en modo lectura (bloqueante)
    respuesta = os.read(fr, 1024).decode().strip()  # Leer del FIFO
    
    if respuesta == "/exit":
        print("A ha salido del chat.")
        os.close(fr)
        break
    
    print(f"A: {respuesta}")  # Mostrar mensaje de A
    os.close(fr)  # Cerrar el FIFO después de leer

    # Enviar mensaje
    fw = os.open(fifo_write, os.O_WRONLY)  # Abrir FIFO en modo escritura (bloqueante)
    msg = input("B: ")  # El usuario ingresa un mensaje
    
    if msg == "/exit":
        os.write(fw, b"/exit")
        os.close(fw)
        break
    
    msg = '[' + datetime.now().strftime("%H:%M:%S") + '] ' + msg + '\n'
    os.write(fw, msg.encode())  # Escribir el mensaje en el FIFO
    os.close(fw)  # Cerrar el FIFO después de escribir
