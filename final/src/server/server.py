import asyncio
import json
import time
import socket
from celery.result import AsyncResult

from src.worker.celery_app import app as celery_app
from src.worker.tasks import process_large_chunk

from src.server.aggregator import aggregate_final_stats

from src.shared.utils import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    split_list_into_chunks,
    PROCESSING_WORKERS, # Número de workers (chunks) a usar
    RESULTS_TIMEOUT, # Timeout global para esperar resultados
)


async def _wait_for_one_task(async_result: AsyncResult):
    """Espera (pasivamente) a que un resultado de Celery esté listo."""
    try:
        # Esto es ahora una "espera pasiva" (bloqueante en un hilo separado)
        result = await asyncio.to_thread(async_result.get, timeout=RESULTS_TIMEOUT)
        return result
    except Exception as e:
        # Si el .get() falla (por ej: por timeout de Celery), capturamos el error
        print(f"[SERVER] Error en un worker: {e}")
        raise


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
        chunk_size = (len(lines) + PROCESSING_WORKERS - 1) // PROCESSING_WORKERS

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

        # Espera de resultados con timeout global
        try:
            # Creamos una lista de corrutinas, una para cada tarea
            # Usamos celery_app.AsyncResult para asegurar que se use la configuración de la app
            waiter_coroutines = [
                _wait_for_one_task(celery_app.AsyncResult(task_id))
                for task_id in task_ids
            ]

            print(
                f"[SERVER] Esperando {len(waiter_coroutines)} resultados con un timeout de {RESULTS_TIMEOUT}s..."
            )

            # asyncio.gather corre todas las corrutinas concurrentemente

            # asyncio.wait_for le pone un límite de tiempo a la espera total
            results = await asyncio.wait_for(
                asyncio.gather(*waiter_coroutines), timeout=RESULTS_TIMEOUT
            )
            print("[SERVER] Todas las tareas completadas.")

        except asyncio.TimeoutError:
            # Si se agota el tiempo de espera, envía una respuesta de error clara al cliente.
            error_response = {
                "error": f"Timeout: Los workers no respondieron en {RESULTS_TIMEOUT}s.",
                "suggestion": "El archivo puede ser demasiado grande o los workers están sobrecargados. Intente nuevamente más tarde o con un archivo más pequeño.",
            }
            writer.write(json.dumps(error_response, indent=2, ensure_ascii=False).encode("utf-8")) # Para legibilidad
            await writer.drain()
            # Se retorna para evitar que el error sea capturado por el manejador de excepciones general.
            return

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
    Función principal que inicia el servidor asyncio, con soporte para dual-stack (IPv4/IPv6).
    """
    listen_sockets = []

    try:
        # Para obtener los protocolos disponibles (IPv4, IPv6 o ambos)
        addr_info = await asyncio.get_event_loop().getaddrinfo(
            DEFAULT_HOST,
            DEFAULT_PORT,
            family=socket.AF_UNSPEC,
            type=socket.SOCK_STREAM,
            flags=socket.AI_PASSIVE,  # Socket pasivo (no se conecta a nadie, solo escucha)
        )
    except socket.gaierror as e:
        print(f"[SERVER] Error al obtener información de la dirección: {e}")
        return

    # Creamos un socket segun los protocolos disponibles (uno, otro o ambos)
    for response in addr_info:
        family, socktype, proto, _, sockaddr = response
        try:
            sock = socket.socket(family, socktype, proto)
            sock.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
            )  # Direccion reusable

            # Forzar el socket IPv6 a ser solo IPv6
            if family == socket.AF_INET6:
                sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)

            sock.bind(sockaddr)
            listen_sockets.append(sock)  # Llevamos una lista de los sockets pasivos

        except OSError as e:
            print(f"[SERVER] No se pudo bindear a {sockaddr}: {e}")
            if sock:
                sock.close()
            continue

    if not listen_sockets:
        print("[SERVER] No se pudo crear ningún socket de escucha. Abortando.")
        return

    servers = []
    for sock in listen_sockets:
        server = await asyncio.start_server(
            handle_client,
            sock=sock,
        )
        servers.append(server)

    # Juntamos todas las direcciones de todos los servidores creados para el print de log
    all_addrs = []
    for server in servers:
        for sock in server.sockets:
            all_addrs.append(str(sock.getsockname()))

    print(f"[SERVER] Escuchando en {', '.join(all_addrs)}...")
    print("[SERVER] Esperando conexiones...")

    await asyncio.gather(*(server.serve_forever() for server in servers))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:  # Para cerrar con Ctrl+C
        print("\n[SERVER] Servidor detenido por el usuario.")
