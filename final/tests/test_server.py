import asyncio
import json
from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from src.server.server import handle_client

pytestmark = pytest.mark.asyncio

@patch("src.server.server.aggregate_final_stats")
@patch("src.server.server.AsyncResult")
@patch("src.server.server.process_large_chunk")
@patch("src.server.server.time")
@patch("src.server.server.asyncio.sleep", new_callable=AsyncMock)
class TestHandleClient:
    async def test_full_flow_with_polling(
        self, mock_sleep, mock_time, mock_process_chunk, mock_async_result, mock_aggregator
    ):
        # ... (Misma lógica que el test_handle_client_full_flow_with_polling)
        mock_time.time.side_effect = [1000.0, 1010.5]
        mock_task_1, mock_task_2, mock_task_3 = MagicMock(id="t1"), MagicMock(id="t2"), MagicMock(id="t3")
        mock_process_chunk.delay.side_effect = [mock_task_1, mock_task_2, mock_task_3]
        mock_result_1, mock_result_2, mock_result_3 = MagicMock(), MagicMock(), MagicMock()
        mock_result_1.ready.side_effect = [False, True]
        mock_result_1.get.return_value = {"msg": 1}
        mock_result_2.ready.side_effect = [False, False, True]
        mock_result_2.get.return_value = {"msg": 2}
        mock_result_3.ready.return_value = True
        mock_result_3.get.return_value = {"msg": 3}
        mock_async_result.side_effect = [mock_result_1, mock_result_2, mock_result_3]
        mock_aggregator.return_value = {"final_messages": 100, "workers_used": 3}
        test_chat_data = b"linea 1\nlinea 2\nlinea 3\nlinea 4\nlinea 5"
        mock_reader = AsyncMock(spec=asyncio.StreamReader)
        mock_reader.read.return_value = test_chat_data
        mock_writer = MagicMock(spec=asyncio.StreamWriter)
        mock_writer.drain = AsyncMock()
        mock_writer.wait_closed = AsyncMock()
        mock_writer.get_extra_info.return_value = ("127.0.0.1", 12345)

        await handle_client(mock_reader, mock_writer)

        assert mock_process_chunk.delay.call_count == 3
        assert mock_sleep.call_count == 3
        mock_aggregator.assert_called_once_with([{"msg": 1}, {"msg": 2}, {"msg": 3}])
        mock_writer.write.assert_called_once()
        response_json = json.loads(mock_writer.write.call_args[0][0].decode("utf-8"))
        assert response_json["final_messages"] == 100
        assert response_json["processing_time"] == 10.5

    async def test_no_data(
        self, mock_sleep, mock_time, mock_process_chunk, mock_async_result, mock_aggregator
    ):
        mock_reader = AsyncMock(spec=asyncio.StreamReader)
        mock_reader.read.return_value = b""
        mock_writer = MagicMock(spec=asyncio.StreamWriter)
        mock_writer.wait_closed = AsyncMock()
        mock_writer.get_extra_info.return_value = ("127.0.0.1", 12345)

        await handle_client(mock_reader, mock_writer)

        mock_writer.write.assert_not_called()
        mock_writer.close.assert_called_once()
        mock_writer.wait_closed.assert_called_once()

    async def test_empty_file(
        self, mock_sleep, mock_time, mock_process_chunk, mock_async_result, mock_aggregator
    ):
        mock_reader = AsyncMock(spec=asyncio.StreamReader)
        mock_reader.read.return_value = b"\n \t \n"
        mock_writer = MagicMock(spec=asyncio.StreamWriter)
        mock_writer.wait_closed = AsyncMock()
        mock_writer.get_extra_info.return_value = ("127.0.0.1", 12345)

        await handle_client(mock_reader, mock_writer)

        mock_writer.write.assert_called_once()
        written_data = mock_writer.write.call_args[0][0].decode("utf-8")
        assert "error" in written_data.lower()
        mock_writer.close.assert_called_once()

    async def test_exception_handling(
        self, mock_sleep, mock_time, mock_process_chunk, mock_async_result, mock_aggregator
    ):
        mock_time.time.side_effect = [1000.0, 1010.5]
        mock_process_chunk.delay.return_value = MagicMock(id="t1")
        mock_async_result.return_value = MagicMock(ready=lambda: True, get=lambda: {"msg": 1})
        mock_aggregator.side_effect = Exception("KABOOM")
        mock_reader = AsyncMock(spec=asyncio.StreamReader)
        mock_reader.read.return_value = b"linea 1\nlinea 2"
        mock_writer = MagicMock(spec=asyncio.StreamWriter)
        mock_writer.drain = AsyncMock()
        mock_writer.wait_closed = AsyncMock()
        mock_writer.get_extra_info.return_value = ("127.0.0.1", 12345)

        await handle_client(mock_reader, mock_writer)

        mock_aggregator.assert_called_once()
        mock_writer.write.assert_called_once()
        response_json = json.loads(mock_writer.write.call_args[0][0].decode("utf-8"))
        assert "error" in response_json
        assert response_json["error"] == "KABOOM"
        mock_writer.close.assert_called_once()



async def test_server_startup_and_dual_stack():
    """
    Test de integración que inicia un servidor real en un puerto aleatorio
    y verifica la conectividad dual-stack.
    """
    from src.server.server import main as server_main

    # Iniciar el servidor en una tarea de fondo
    server_task = asyncio.create_task(server_main())
    
    # Darle un momento para que arranque
    await asyncio.sleep(0.1)

    # Obtener el puerto asignado por el sistema operativo (puerto 0)
    # Esto es más robusto que usar un puerto fijo que podría estar en uso.
    # Sin embargo, para este test, usaremos el puerto por defecto y asumiremos que está libre.
    port = 8888

    try:
        # Probar conexión IPv4
        try:
            reader_v4, writer_v4 = await asyncio.open_connection("127.0.0.1", port)
            writer_v4.close()
            await writer_v4.wait_closed()
            print("Conexión IPv4 exitosa.")
        except ConnectionRefusedError:
            pytest.fail("La conexión IPv4 fue rechazada.")

        # Probar conexión IPv6
        try:
            reader_v6, writer_v6 = await asyncio.open_connection("::1", port)
            writer_v6.close()
            await writer_v6.wait_closed()
            print("Conexión IPv6 exitosa.")
        except ConnectionRefusedError:
            pytest.fail("La conexión IPv6 fue rechazada.")

    finally:
        # Detener el servidor
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass  # Esperado


@patch("src.server.server.asyncio.gather")
@patch("src.server.server.AsyncResult")
@patch("src.server.server.process_large_chunk")
async def test_handle_client_timeout(mock_process_chunk, mock_async_result, mock_gather):
    """
    Test que simula un asyncio.TimeoutError durante el polling de Celery.
    """
    # Configurar mocks
    mock_process_chunk.delay.return_value = MagicMock(id="t1")
    mock_async_result.return_value = MagicMock()
    
    # Simular que asyncio.gather nunca termina, lo que causará el timeout
    # en el asyncio.wait_for que lo envuelve en el código de producción.
    mock_gather.side_effect = asyncio.TimeoutError("Simulated timeout")

    mock_reader = AsyncMock(spec=asyncio.StreamReader)
    mock_reader.read.return_value = b"linea 1\nlinea 2"
    mock_writer = MagicMock(spec=asyncio.StreamWriter)
    mock_writer.drain = AsyncMock()
    mock_writer.wait_closed = AsyncMock()
    mock_writer.get_extra_info.return_value = ("127.0.0.1", 12345)

    # Llamar a la función
    await handle_client(mock_reader, mock_writer)

    # Verificar que se envió un mensaje de error
    mock_writer.write.assert_called_once()
    response_json = json.loads(mock_writer.write.call_args[0][0].decode("utf-8"))
    assert "error" in response_json
    assert "Tiempo de espera agotado" in response_json["error"]
    mock_writer.close.assert_called_once()