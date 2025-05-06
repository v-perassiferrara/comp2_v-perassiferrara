
'''
Ejercicio 5: Simulación de cola de trabajos con señales
Objetivo: Simular un sistema productor-consumidor asíncrono usando señales.

Enunciado: Desarrolla dos procesos: uno productor y uno consumidor.

El productor genera trabajos (simulados por mensajes con timestamp) y,
al generarlos, envía SIGUSR1 al consumidor.

El consumidor debe recibir la señal,
registrar el timestamp de recepción y "procesar" el trabajo (simulado con un sleep()).

Implementa una protección contra pérdida de señales: si se reciben varias en rápida sucesión,
deben encolarse en una estructura temporal para ser procesadas una por una.

(para esto último se encolan todas las señales independientemente de si llegaron en rápida sucesión o no)
'''





import os, signal, time, sys
from datetime import datetime

# Cola local en el consumidor para almacenar trabajos pendientes
pendientes = []

def handler_sigusr1(signum, frame):
    # Al recibir SIGUSR1, encolamos el timestamp para que sea procesado luego
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pendientes.append(timestamp)
    
    # Imprimimos el timestamp para ver que se ha recibido la señal
    print(f"\n[CONSUMIDOR] Señal recibida, añadido trabajo {timestamp}")

# Creamos el proceso hijo (consumidor), el padre es el productor
pid = os.fork()

if pid == 0:
    # CONSUMIDOR
    signal.signal(signal.SIGUSR1, handler_sigusr1)  # Asignar handler para SIGUSR1
    print(f"\n[CONSUMIDOR] {os.getpid()} esperando trabajos…")

    try:
        while True:
            # Si hay trabajos pendientes, procesamos uno por uno
            if pendientes:
                timestamp_trabajo = pendientes.pop(0)  # sacamos el primer trabajo de la queue
                print(f"\n[CONSUMIDOR] Procesando {timestamp_trabajo}")
                time.sleep(1)  # simulación de procesamiento
                print(f"\n[CONSUMIDOR] Trabajo finalizado ({timestamp_trabajo})")
            else:
                # si no hay nada, esperamos un poco antes de revisar de nuevo
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[CONSUMIDOR] Terminando por teclado.")
        sys.exit(0)

else:
    # PRODUCTOR
    pid_consumidor = pid
    print(f"\n[PRODUCTOR] {os.getpid()} generará trabajos para consumidor={pid_consumidor}")

    try:
        for i in range(10):  # 10 trabajos de ejemplo
            time.sleep(0.5)  # Simulación de tiempo entre trabajos
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n[PRODUCTOR] Creado trabajo {i+1}: {timestamp}")
            os.kill(pid_consumidor, signal.SIGUSR1)  # Enviar SIGUSR1 para notificar al consumidor
        print("\n[PRODUCTOR] Todos los trabajos enviados. Saliendo.")
    except KeyboardInterrupt:
        print("\n[PRODUCTOR] Interrumpido por teclado.")
    finally:
        sys.exit(0)

