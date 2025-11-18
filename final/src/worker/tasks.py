import multiprocessing

from src.shared.utils import split_list_into_chunks, SUB_CHUNK_SIZE, PROCESSING_WORKERS
from src.worker.celery_app import app
from src.worker.consolidator import consolidate_results
from src.worker.parser import extract_stats_from_subchunk


# Forzamos "spawn": crea un proceso hijo limpio
# Esto evita errores de IPC cuando el Pool se crea desde un hilo
# (worker de Celery con --pool=threads)
mp_context = multiprocessing.get_context("spawn")


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
        print(f"Error procesando sub-chunk: {e}")
        result_queue.put(None)  # Poner None para que el consolidador no se bloquee
    finally:
        # Al usar un value de manager, no es necesario un lock explícito
        processed_counter.value += 1


@app.task()
def process_large_chunk(chunk_data):
    """
    Tarea de Celery que procesa un chunk grande de líneas de chat.
    Utiliza un multiprocessing.Pool para paralelizar el trabajo a nivel local.
    """
    lines = chunk_data.splitlines()
    if not lines:
        return {}

    # Dividir el chunk grande en sub-chunks más pequeños
    sub_chunks = split_list_into_chunks(lines, SUB_CHUNK_SIZE)
    num_sub_chunks = len(sub_chunks)

    # Usamos el Manager del contexto "spawn" para poder compartir queue y value
    with mp_context.Manager() as manager:
        # Queue y Value compartidos entre procesos para contar los sub-chunks procesados y enviar los resultados
        result_queue = manager.Queue()
        processed_counter = manager.Value("i", 0)  # "i" = integer, 0 = valor inicial

        # Crear y usar el Pool de procesos
        # Usamos el Pool del contexto "spawn"
        with mp_context.Pool(processes=PROCESSING_WORKERS) as pool:
            # Preparamos los argumentos para cada llamada
            # starmap requiere una lista de tuplas: [(arg1, arg2, ...), (arg1, arg2, ...)]
            task_args = []
            for sub_chunk in sub_chunks:
                task_args.append((sub_chunk, result_queue, processed_counter))

            # starmap es bloqueante: ejecuta todas las tareas en el pool
            # y no continúa hasta que TODAS hayan terminado.
            pool.starmap(_process_sub_chunk_wrapper, task_args)

        # En este punto, TODAS las tareas del pool terminaron y el pool se cerro.
        # El `processed_counter` esta en su valor final.
        # La `result_queue` esta llena con todos los resultados.

        # Una vez que todos los sub-chunks han sido enviados, consolidamos los resultados
        print(f"Consolidando resultados de {num_sub_chunks} sub-chunks...")
        final_stats = consolidate_results(result_queue, num_sub_chunks)

    return final_stats
