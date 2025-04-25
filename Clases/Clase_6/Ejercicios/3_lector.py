'''
Ejercicio 3 — FIFO + archivos
Objetivo: Usar un FIFO como entrada para un proceso que guarda datos en un archivo.

Instrucciones:

Crear un script que escuche un FIFO y guarde todo lo que llega en output.txt.
Otro script debe leer líneas desde el teclado y enviarlas al FIFO.
Al escribir "exit" se debe cerrar todo correctamente.
'''

import os, sys

fifo = 'fifo_prueba3'
# Asegurarse de que exista
try:
    os.mkfifo(fifo)
except FileExistsError:
    pass

print("Abriendo FIFO para lectura…")
with open(fifo, 'r') as f:
    
    # Abrimos el archivo en modo append para no sobreescribir
    with open('output.txt', 'a') as output_file:
        for linea in iter(f.readline, ''):
            # Si la línea es "exit", cerramos el archivo y salimos
            if linea.strip() == "exit":
                print("Cerrando y saliendo…")
                break
            output_file.write(linea.strip() + '\n')
            print(f"Recibido y guardado: {linea.strip()}")
