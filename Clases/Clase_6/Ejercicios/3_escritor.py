'''
Ejercicio 3 — FIFO + archivos
Objetivo: Usar un FIFO como entrada para un proceso que guarda datos en un archivo.

Instrucciones:

Crear un script que escuche un FIFO y guarde todo lo que llega en output.txt.
Otro script debe leer líneas desde el teclado y enviarlas al FIFO.
Al escribir "exit" se debe cerrar todo correctamente.
'''

import os, time

fifo = 'fifo_prueba3'
# Asegurarse de que exista
try:
    os.mkfifo(fifo)
except FileExistsError:
    pass

msg = ""

print("Abriendo FIFO para escritura…")
with open(fifo, 'w') as f:
    while msg != "exit":
        msg = str(input("Escriba un mensaje: "))
        f.write(msg)
        f.flush()
        print(f"Enviado: {msg.strip()}")
        time.sleep(1)
    
