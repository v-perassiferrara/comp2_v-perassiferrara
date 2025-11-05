from src.worker.tasks import process_large_chunk, _process_sub_chunk_wrapper
from multiprocessing import Manager


def test_process_sub_chunk_wrapper():
    """
    Unit test for the wrapper function around the parsing logic.
    """
    sub_chunk_lines = [
        "27/03/2024, 09:17 - Julián (Soporte): Estamos ajustando la carga del servidor. Te aviso cuando normalice.",
        "27/03/2024, 11:02 - +54 9 11 3987-1951: El sistema me desconecta cada 10 minutos.",
    ]

    result_queue = Manager().Queue()
    processed_counter = Manager().Value("i", 0)

    _process_sub_chunk_wrapper(sub_chunk_lines, result_queue, processed_counter)

    # Assertions for the consolidated result
    result = result_queue.get()
    assert result["total_messages"] == 2
    assert result["users"] == {
        "Julián (Soporte)": 1,
        "+54 9 11 3987-1951": 1,
    }
    assert result["hourly_distribution"] == {"09": 1, "11": 1}
    assert result["daily_distribution"] == {"Miércoles": 2}


def test_process_large_chunk():
    """
    Unit test for the main task.
    """
    chunk_data = (
        "27/03/2024, 09:17 - Julián (Soporte): Estamos ajustando la carga del servidor. Te aviso cuando normalice.\n"
        "27/03/2024, 11:02 - +54 9 11 3987-1951: El sistema me desconecta cada 10 minutos.\n"
    )

    result = process_large_chunk(chunk_data)

    # Assertions for the consolidated result
    assert result["total_messages"] == 2
    assert result["users"] == {
        "Julián (Soporte)": 1,
        "+54 9 11 3987-1951": 1,
    }
    assert result["hourly_distribution"] == {"09": 1, "11": 1}
    assert result["daily_distribution"] == {"Miércoles": 2}


def test_process_large_chunk_empty_and_invalid_input():
    """Test that the main task handles empty or invalid data chunks."""
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
