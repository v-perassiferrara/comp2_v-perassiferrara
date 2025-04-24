'''
3) Patrón Distribuido:
    Diseña un sistema en el que la cola se utilice para distribuir tareas a un grupo de procesos trabajadores, y luego recopila los resultados en otra cola para el procesamiento final.
'''

import os
import time
from multiprocessing import Queue
from queue import Empty

def trabajador(q_tareas, q_resultados, id_trabajador):
    print(f"Trabajador {id_trabajador} arrancando…")
    while True:
        try:
            tarea = q_tareas.get(timeout=2)
        except Empty:
            continue
        if tarea == "FIN":
            break
        # Simula procesamiento
        resultado = f"Resultado T{id_trabajador} de {tarea}"
        print(f"Trabajador {id_trabajador} realizó {tarea}")
        time.sleep(0.5)
        q_resultados.put(resultado)
        
    print(f"Trabajador {id_trabajador} terminado.")

def main():
    q_tareas   = Queue()
    q_resultados = Queue()
    num_trabajadores   = 2
    num_tareas  = 4

    # Crear procesos trabajadores
    for i in range(num_trabajadores): 
        pid = os.fork()
        if pid == 0:
            trabajador(q_tareas, q_resultados, i)
            os._exit(0)

    # Padre manda tareas
    for j in range(1, num_tareas+1):
        tarea = f"Tarea {j}"
        q_tareas.put(tarea)
        print(f"Main cargó {tarea}")
        
    # Señal de fin para cada trabajador
    for _ in range(num_trabajadores):
        q_tareas.put("FIN")

    # Padre recoge resultados
    recogidos = 0
    while recogidos < num_tareas:
        try:
            num_recibidos = q_resultados.get(timeout=5)
        except Empty:
            continue
        print(f"Main recibió {num_recibidos}")
        recogidos += 1

    # Espera a los trabajadores
    for _ in range(num_trabajadores):
        os.wait()
    print("Fin de la comunicación.")

if __name__ == "__main__":
    main()
