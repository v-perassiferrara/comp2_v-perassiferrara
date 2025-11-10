import asyncio
import json
import time
from celery.result import AsyncResult

from src.worker.celery_app import app as celery_app
from src.worker.tasks import process_large_chunk

from src.server.aggregator import aggregate_final_stats

from src.shared.utils import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    split_list_into_chunks,
)

# Número de workers/chunks a usar
NUM_WORKERS = 4
POLLING_TIMEOUT = 120  # 2 minutos de espera máxima en total, para evitar que se cuelgue


async def _wait_for_one_task(async_result: AsyncResult):
    """Espera a que un resultado de Celery esté listo."""
    while not async_result.ready():
        await asyncio.sleep(1.0)
    return async_result.get()


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """
    Esta corrutina se corre para cada nuevo cliente que se conecta, y gestiona
    su interacción completa
    """

    addr = writer.get_extra_info("peername")
    print(f"[SERVER] Cliente conectado desde {addr}")

    start_time = time.time()

    try:
        # Recibir archivo

        print(f"[SERVER] Esperando datos de {addr}...")

        # Leer desde el reader hasta EOF (cliente cierra escritura)
        data = await reader.read()
        if not data:
            print(f"[SERVER] Cliente {addr} no envió datos.")
            return

        full_chat_content = data.decode("utf-8")
        print(f"[SERVER] Recibidas {len(full_chat_content)} bytes de chat.")

        # Dividir en chunks

        lines = full_chat_content.splitlines()
        if not lines:
            print("[SERVER] El archivo de chat está vacío.")
            return

        # Calcular el número de líneas por chunk para obtener el numero de chunks deseado
        chunk_size = (len(lines) + NUM_WORKERS - 1) // NUM_WORKERS

        # Dividir la lista líneas en chunks (listas de listas)
        line_chunks = split_list_into_chunks(lines, chunk_size)

        # Unir las líneas de cada chunk de nuevo a un string para mandar a Celery
        large_chunks = ["\n".join(chunk) for chunk in line_chunks]

        print(f"[SERVER] Archivo dividido en {len(large_chunks)} chunks.")

        # Despachar tareas a Celery

        task_ids = []
        for chunk_data_str in large_chunks:
            task = process_large_chunk.delay(chunk_data_str)  # Manda a Celery
            task_ids.append(task.id)  # Guardamos el ID para seguimiento

        print(f"[SERVER] Tareas despachadas a Celery: {task_ids}")

        # Polling de resultados con timeout global
        try:
            # Creamos una lista de corrutinas, una para cada tarea
            waiter_coroutines = [
                _wait_for_one_task(AsyncResult(task_id, app=celery_app))
                for task_id in task_ids
            ]

            print(
                f"[SERVER] Esperando {len(waiter_coroutines)} resultados con un timeout de {POLLING_TIMEOUT}s..."
            )

            # asyncio.gather corre todas las corrutinas concurrentemente

            # asyncio.wait_for le pone un límite de tiempo a la espera total
            results = await asyncio.wait_for(
                asyncio.gather(*waiter_coroutines), timeout=POLLING_TIMEOUT
            )
            print("[SERVER] Todas las tareas completadas.")

        except asyncio.TimeoutError:
            # Si se agota el tiempo de espera, salta una excepción que será
            # capturada por el manejador de errores principal de la función.
            raise Exception(
                f"Tiempo de espera agotado ({POLLING_TIMEOUT}s) para recibir la respuesta de los workers."
            )

        # Unificar resultados con el agregador

        print("[SERVER] Todos los resultados recibidos. Agregando stats finales...")
        final_stats = aggregate_final_stats(results)

        # Agregamos metrica extra de rendimiento (tiempo de procesamiento)
        processing_time = time.time() - start_time
        final_stats["processing_time"] = round(processing_time, 2)

        # Respuesta final al cliente
        # indent y ensure_ascii para mejor legibilidad
        response_data = json.dumps(final_stats, indent=2, ensure_ascii=False).encode(
            "utf-8"
        )

        writer.write(response_data)
        await writer.drain()

        print(f"[SERVER] Respuesta enviada a {addr}")

    except Exception as e:
        print(f"[SERVER] Error manejando al cliente {addr}: {e}")

        # Si falla, retorna un mensaje de error al cliente
        error_msg = json.dumps({"error": str(e)}).encode("utf-8")
        writer.write(error_msg)
        await writer.drain()

    finally:  # Cerramos la conexión
        print(f"[SERVER] Cerrando conexión con {addr}")
        writer.close()
        await writer.wait_closed()


async def main():
    """
    Función principal que inicia el servidor asyncio.
    """
    server = await asyncio.start_server(handle_client, DEFAULT_HOST, DEFAULT_PORT)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"[SERVER] Escuchando en {addrs} (Puerto {DEFAULT_PORT})...")
    print("[SERVER] Esperando conexiones...")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:  # Para cerrar con Ctrl+C
        print("\n[SERVER] Servidor detenido por el usuario.")
