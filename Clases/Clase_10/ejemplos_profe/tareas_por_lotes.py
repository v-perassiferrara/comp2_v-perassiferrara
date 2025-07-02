import threading
from multiprocessing import JoinableQueue
import queue
import time
import random

NUM_TASK_PROCESSORS = 3
NUM_TASKS = 15
STOP_SIGNAL = "---ALL_TASKS_PROCESSED_STOP---" # Señal para el registrador

def task_processor(task_queue, result_queue, processor_id):
    """ Toma tareas de task_queue, las procesa y pone resultados en result_queue. """
    print(f"Procesador {processor_id}: Iniciado.")
    while True:
        try:
            # Obtiene una tarea de la cola, espera máximo 1 segundo si está vacía
            task = task_queue.get(timeout=1) 
            
            if task is None: # Señal de fin para este procesador
                print(f"Procesador {processor_id}: Señal de fin recibida. Terminando.")
                task_queue.task_done() # Importante para JoinableQueue si se usa
                break
            
            print(f"Procesador {processor_id}: Procesando '{task}'...")
            time.sleep(random.uniform(0.5, 1.5)) # Simula procesamiento
            result = f"Resultado de '{task}' por Procesador {processor_id}"
            result_queue.put(result)
            task_queue.task_done() # Importante para JoinableQueue si se usa

        except queue.Empty:
            # Esto puede ocurrir si el timeout se alcanza y no hay tareas
            # Podríamos decidir si el procesador debe terminar o seguir esperando.
            # En este caso, como usamos señales 'None', asumimos que si está vacía
            # y no hay señal None, llegarán más tareas o la señal.
            print(f"Procesador {processor_id}: Cola de tareas vacía, esperando de nuevo...")
            continue # Vuelve al inicio del while
    print(f"Procesador {processor_id}: Finalizado.")


def result_logger(result_queue, log_file_name="task_log.txt"):
    """ Toma resultados de result_queue y los escribe en un archivo/consola. """
    print("Registrador: Iniciado.")
    processed_count = 0
    with open(log_file_name, "w") as f: # Abre en modo escritura para limpiar log anterior
        while True:
            try:
                result = result_queue.get(timeout=1)
                if result == STOP_SIGNAL:
                    print("Registrador: Señal de fin recibida. Terminando.")
                    f.write("--- FIN DEL REGISTRO ---\n")
                    result_queue.task_done()
                    break
                
                log_entry = f"{time.ctime()}: {result}\n"
                print(f"Registrador: {result}")
                f.write(log_entry)
                processed_count +=1
                result_queue.task_done() # Para JoinableQueue
            except queue.Empty:
                # Podría indicar que no hay más resultados O que los procesadores aún no terminan.
                # La señal STOP_SIGNAL es la que determina el fin.
                pass
    print(f"Registrador: Finalizado. Total de resultados registrados: {processed_count}")


if __name__ == "__main__":
    # Usaremos JoinableQueue para la cola de tareas para poder esperar a que se procesen todas.
    # queue.Queue normal para resultados es suficiente aquí.
    tasks_to_do = JoinableQueue()
    results_done = JoinableQueue() # También Joinable para esperar al logger

    # Hilos procesadores
    processor_threads = []
    for i in range(NUM_TASK_PROCESSORS):
        pt = threading.Thread(target=task_processor, args=(tasks_to_do, results_done, i), daemon=True)
        processor_threads.append(pt)
        pt.start()

    # Hilo registrador
    logger_thread = threading.Thread(target=result_logger, args=(results_done,), daemon=True)
    logger_thread.start()

    # Poner tareas en la cola
    print(f"\nPrincipal: Añadiendo {NUM_TASKS} tareas a la cola...")
    for i in range(NUM_TASKS):
        tasks_to_do.put(f"Tarea-{i+1}")
    print("Principal: Todas las tareas añadidas.")

    # Poner señales de fin para los procesadores
    for _ in range(NUM_TASK_PROCESSORS):
        tasks_to_do.put(None) # Un 'None' por cada procesador
    print("Principal: Señales de fin para procesadores añadidas.")

    # Esperar a que todas las tareas en tasks_to_do sean obtenidas y procesadas
    # (task_done() llamado para cada una)
    print("Principal: Esperando a que todas las tareas sean procesadas...")
    tasks_to_do.join()
    print("Principal: Todas las tareas han sido procesadas por los workers.")

    # Señal de fin para el registrador
    print("Principal: Enviando señal de fin al registrador...")
    results_done.put(STOP_SIGNAL)

    # Esperar a que el registrador procese todos los resultados (incluyendo la señal STOP)
    print("Principal: Esperando al registrador...")
    results_done.join()
    print("Principal: Registrador ha terminado.")
    
    # Aunque los hilos son daemon, un join explícito puede ser bueno para limpieza final si fuera necesario.
    # Aquí, JoinableQueue.join() ya nos da una buena sincronización de finalización.
    # No es estrictamente necesario esperar a los hilos daemon si la lógica de JoinableQueue es suficiente.
    # for pt in processor_threads:
    #     pt.join(timeout=2) # Espera un poco por si acaso
    # logger_thread.join(timeout=2)


    print("\nSimulación completada. Revisa 'task_log.txt'.")