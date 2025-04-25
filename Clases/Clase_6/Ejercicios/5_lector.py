'''
Ejercicio 5 — FIFO con apertura condicional
Objetivo: Usar os.open() y manejar errores.

Instrucciones:

Usar os.open() con flags como O_NONBLOCK.
Crear un lector que intente abrir el FIFO sin bloquear.
Si el FIFO no tiene escritores, debe imprimir un mensaje y salir correctamente.
Desafío adicional: Hacer que el lector reintente 5 veces con espera entre intentos antes de salir.
'''

import os, time, select

fifo = '/tmp/fifo_errores'
try:
    os.mkfifo(fifo)
except FileExistsError:
    pass

# Intentos de lectura
intentos = 0

# Abrimos el FIFO en modo lectura no bloqueante
# O_RDONLY: Abrimos el FIFO en modo de solo lectura
# O_NONBLOCK: No bloqueamos a la espera de que haya datos en el FIFO
# Si no hay datos, devolvemos un error EAGAIN (Resource temporarily unavailable)
fifo = os.open('/tmp/fifo_errores', os.O_RDONLY | os.O_NONBLOCK)

# Bucle principal
while intentos < 5:
    # Select es una llamada al sistema que nos permite esperar a que haya datos
    # en el FIFO. Si no los hay, devuelve una lista vacía.
    # rlist: lista de descriptores de archivos que tienen datos (de lectura)
    # wlist: lista de descriptores de archivos que pueden escribir (de escritura) (no usada)
    # xlist: lista de descriptores de archivos que tienen una exception (de excepciones) (no usada)
    # timeout: segundos a esperar a que haya datos (en este caso, 1 segundo)
    rlist, _, _ = select.select([fifo], [], [], 1) 

    # Si hay datos, los leemos
    if rlist:
        data = os.read(fifo, 1024)
        if not data:
            print("No hay más datos, cerrando lector.")
            break
        print(f"Recibido: {data.decode()}")
    else:
        print(f"No hay escritores disponibles, esperando... [Intento {intentos+1}]")
        intentos += 1
        time.sleep(1)
    
print("No se encontraron escritores, cerrando lector.")
