from multiprocessing import Pool, Queue, Value

from src.worker.celery_app import app
from src.worker.consolidator import consolidate_results
from src.worker.parser import extract_stats_from_subchunk

# Constantes
SUB_CHUNK_SIZE = 1000  # Líneas por sub-proceso
MAX_WORKERS = 4  # Número de procesos en el Pool


def _process_sub_chunk_wrapper(sub_chunk_lines, result_queue, processed_counter):
    """
    Wrapper que se ejecuta en cada proceso del Pool.
    Llama al parser y pone el resultado en la cola compartida (procesa un sub-chunk).
    """
    try:
        stats = extract_stats_from_subchunk(sub_chunk_lines)
        result_queue.put(stats)
    except Exception as e:
        # En caso de un error en el sub-proceso, lo reportamos y continuamos
        print(f"Error processing sub-chunk: {e}")
        result_queue.put(None)  # Poner None para que el consolidador no se bloquee
    finally:
        # Incrementa el contador de chunks procesados (lock para sincronización y evitar race conditions)

        with processed_counter.get_lock():
            processed_counter.value += 1


@app.task(bind=True)  # bind=True para acceder a self si es necesario
def process_large_chunk(self, chunk_data):
    """
    Tarea de Celery que procesa un chunk grande de líneas de chat.
    Utiliza un multiprocessing.Pool para paralelizar el trabajo a nivel local.
    """
    lines = chunk_data.splitlines()
    if not lines:
        return {}

    # Dividir el chunk grande en sub-chunks más pequeños
    sub_chunks = [
        lines[i : i + SUB_CHUNK_SIZE] for i in range(0, len(lines), SUB_CHUNK_SIZE)
    ]
    num_sub_chunks = len(sub_chunks)

    # Queue y Value compartidos entre procesos para contar los sub-chunks procesados y enviar los resultados
    result_queue = Queue()
    processed_counter = Value("i", 0)  # "i" = integer, 0 = valor inicial

    # Crear y usar el Pool de procesos
    with Pool(processes=MAX_WORKERS) as pool:
        # Preparamos los argumentos para cada llamada
        # starmap requiere una lista de tuplas: [(arg1, arg2, ...), (arg1, arg2, ...)]
        task_args = []
        for sub_chunk in sub_chunks:
            task_args.append((sub_chunk, result_queue, processed_counter))

        # starmap es bloqueante: ejecuta todas las tareas en el pool
        # y no continúa hasta que TODAS hayan terminado.
        pool.starmap(_process_sub_chunk_wrapper, task_args)

    # En este punto, TODAS las tareas del pool terminaron y el pool se cerró.
    # El `processed_counter` está en su valor final.
    # La `result_queue` está llena con todos los resultados.

    # Una vez que todos los sub-chunks han sido enviados, consolidamos los resultados
    print(f"Consolidating results from {num_sub_chunks} sub-chunks...")
    final_stats = consolidate_results(result_queue, num_sub_chunks)

    return final_stats
