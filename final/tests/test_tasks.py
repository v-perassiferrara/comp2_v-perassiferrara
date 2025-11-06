from src.worker.tasks import process_large_chunk, _process_sub_chunk_wrapper
from multiprocessing import Manager, Value
from unittest.mock import patch


def test_process_sub_chunk_wrapper():
    """
    Unit test for the wrapper function around the parsing logic.
    """
    sub_chunk_lines = [
        "27/03/2024, 09:17 - Julián (Soporte): Estamos ajustando la carga del servidor. Te aviso cuando normalice.",
        "27/03/2024, 11:02 - +54 9 11 3987-1951: El sistema me desconecta cada 10 minutos.",
    ]

    manager = Manager()
    result_queue = manager.Queue()
    # The function expects a Value object with a get_lock method, so we create it directly.
    processed_counter = Value("i", 0)

    _process_sub_chunk_wrapper(sub_chunk_lines, result_queue, processed_counter)

    result = result_queue.get()
    assert result["total_messages"] == 2
    assert result["users"] == {
        "Julián (Soporte)": 1,
        "+54 9 11 3987-1951": 1,
    }
    assert processed_counter.value == 1


def _run_starmap_serially(func, args):
    """Helper to simulate pool.starmap by running tasks in a simple loop."""
    for arg_tuple in args:
        func(*arg_tuple)


@patch("src.worker.tasks.Pool")
def test_process_large_chunk(mock_pool):
    """
    Unit test for the main task, mocking the multiprocessing.Pool
    to avoid environment-specific runtime errors with Queue pickling.
    """
    # The with-statement in the task needs the mock to return a context manager.
    mock_pool_instance = mock_pool.return_value.__enter__.return_value
    # Simulate starmap by running the wrapper function serially in the main thread.
    mock_pool_instance.starmap.side_effect = _run_starmap_serially

    chunk_data = (
        "27/03/2024, 09:17 - Julián (Soporte): Estamos ajustando la carga del servidor. Te aviso cuando normalice.\n"
        "27/03/2024, 11:02 - +54 9 11 3987-1951: El sistema me desconecta cada 10 minutos.\n"
    )

    result = process_large_chunk(chunk_data)

    assert result["total_messages"] == 2
    assert result["users"] == {
        "Julián (Soporte)": 1,
        "+54 9 11 3987-1951": 1,
    }
    assert result["hourly_distribution"] == {"09": 1, "11": 1}
    assert result["daily_distribution"] == {"Miércoles": 2}


@patch("src.worker.tasks.Pool")
def test_process_large_chunk_empty_and_invalid_input(mock_pool):
    """Test that the main task handles empty or invalid data chunks (with Pool mocked)."""
    mock_pool_instance = mock_pool.return_value.__enter__.return_value
    mock_pool_instance.starmap.side_effect = _run_starmap_serially

    # Test with empty string
    empty_result = process_large_chunk("")
    assert empty_result == {}

    # Test with only invalid lines
    invalid_data = (
        "Messages and calls are end-to-end encrypted.\n"
        "\n"
        "Some other system message without a colon."
    )
    invalid_result = process_large_chunk(invalid_data)
    assert invalid_result["total_messages"] == 0
    assert invalid_result["users"] == {}
