import asyncio
import json
from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from src.server.server import handle_client

# Marcador para todas las pruebas en este archivo, para que pytest-asyncio las maneje
pytestmark = pytest.mark.asyncio


@patch("src.server.server.aggregate_final_stats")
@patch("src.server.server.AsyncResult")
@patch("src.server.server.process_large_chunk")
@patch("src.server.server.time")
async def test_handle_client_full_flow(
    mock_time, mock_process_chunk, mock_async_result, mock_aggregator
):
    """
    Test de integración para handle_client, simulando todas las dependencias externas.
    """
    # 1. Configuración de Mocks
    # --- Mock de time para controlar el tiempo de procesamiento ---
    mock_time.time.side_effect = [1000.0, 1010.5]  # Inicio y fin

    # --- Mock de la tarea de Celery ---
    mock_task = MagicMock()
    mock_process_chunk.delay.return_value = mock_task
    mock_task.id = "test-task-id-123"

    # --- Mock del resultado de Celery (AsyncResult) ---
    # Creamos una clase para simular el estado de "listo" de forma más robusta
    class ReadySimulator:
        def __init__(self):
            self.calls = 0
        def __call__(self):
            self.calls += 1
            return self.calls % 2 == 0

    mock_celery_result_instance = MagicMock()
    mock_celery_result_instance.ready.side_effect = ReadySimulator()
    mock_celery_result_instance.get.return_value = {"total_messages": 100}
    mock_async_result.return_value = mock_celery_result_instance

    # --- Mock del agregador final ---
    mock_aggregator.return_value = {"final_messages": 100, "workers_used": 1}

    # 2. Simulación del Cliente (Reader y Writer)
    # --- Datos que el cliente falso envía ---
    test_chat_data = b"linea 1\nlinea 2\nlinea 3"
    # --- Mock del StreamReader ---
    mock_reader = AsyncMock(spec=asyncio.StreamReader)
    mock_reader.read.return_value = test_chat_data

    # --- Mock del StreamWriter ---
    mock_writer = MagicMock(spec=asyncio.StreamWriter)
    # Usamos un AsyncMock para los métodos awaitable
    mock_writer.drain = AsyncMock()
    mock_writer.wait_closed = AsyncMock()
    # Simular get_extra_info para los logs
    mock_writer.get_extra_info.return_value = ("127.0.0.1", 12345)

    # 3. Ejecución de la función a probar
    # En lugar de iniciar un servidor, llamamos directamente a la corrutina
    # que maneja al cliente, pasándole los mocks.
    await handle_client(mock_reader, mock_writer)

    # 4. Verificaciones (Asserts)
    # --- Verificar que se leyó del cliente ---
    mock_reader.read.assert_called_once()

    # --- Verificar que se llamó a Celery ---
    # El número de tareas debe ser igual al número de chunks creados
    num_chunks = len(mock_process_chunk.delay.call_args_list)
    assert mock_process_chunk.delay.call_count == num_chunks

    # --- Verificar que se esperó por el resultado ---
    # ready() se llama 2 veces (False, True) por cada chunk
    assert mock_celery_result_instance.ready.call_count == num_chunks * 2
    assert mock_celery_result_instance.get.call_count == num_chunks

    # --- Verificar que se llamó al agregador con los resultados ---
    mock_aggregator.assert_called_once_with([{"total_messages": 100}] * num_chunks)

    # --- Verificar la respuesta enviada al cliente ---
    mock_writer.write.assert_called_once()
    # Capturar lo que se escribió, decodificarlo y parsearlo
    written_data = mock_writer.write.call_args[0][0]
    response_json = json.loads(written_data.decode("utf-8"))

    # Verificar que el JSON final contiene los datos del agregador y el tiempo
    assert response_json["final_messages"] == 100
    assert response_json["workers_used"] == 1
    assert response_json["processing_time"] == 10.5  # 1010.5 - 1000.0

    # --- Verificar que la conexión se cerró ---
    mock_writer.close.assert_called_once()
    mock_writer.wait_closed.assert_called_once()
