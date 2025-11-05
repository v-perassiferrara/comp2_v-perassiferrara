from multiprocessing import Queue
from collections import Counter
from src.worker.consolidator import consolidate_results

def test_consolidate_results_basic():
    """Test consolidation of multiple valid results."""
    result_queue = Queue()
    total_sub_chunks = 2

    # Mock result from sub-process 1
    result1 = {
        "total_messages": 5,
        "users": Counter({"user1": 3, "user2": 2}),
        "hourly_distribution": Counter({"09": 5}),
        "daily_distribution": Counter({"Lunes": 5}),
        "top_words": Counter({"hola": 3, "mundo": 2}),
    }

    # Mock result from sub-process 2
    result2 = {
        "total_messages": 3,
        "users": Counter({"user1": 1, "user3": 2}),
        "hourly_distribution": Counter({"09": 1, "10": 2}),
        "daily_distribution": Counter({"Lunes": 1, "Martes": 2}),
        "top_words": Counter({"hola": 1, "test": 2}),
    }

    result_queue.put(result1)
    result_queue.put(result2)

    final_stats = consolidate_results(result_queue, total_sub_chunks)

    # Assertions
    assert final_stats["total_messages"] == 8
    assert final_stats["users"] == {"user1": 4, "user2": 2, "user3": 2}
    assert final_stats["hourly_distribution"] == {"09": 6, "10": 2}
    assert final_stats["daily_distribution"] == {"Lunes": 6, "Martes": 2}
    
    top_words_dict = dict(final_stats["top_words"])
    assert top_words_dict["hola"] == 4
    assert top_words_dict["test"] == 2
    assert top_words_dict["mundo"] == 2

def test_consolidate_results_with_empty_or_none():
    """Test that consolidation handles empty or None results gracefully."""
    result_queue = Queue()
    total_sub_chunks = 3

    result1 = {
        "total_messages": 2,
        "users": Counter({"user1": 2}),
        "hourly_distribution": Counter({"14": 2}),
        "daily_distribution": Counter({"Viernes": 2}),
        "top_words": Counter({"gracias": 2}),
    }

    result_queue.put(result1)
    result_queue.put(None)  # Simulate a failed sub-process
    result_queue.put({})    # Simulate an empty result

    final_stats = consolidate_results(result_queue, total_sub_chunks)

    assert final_stats["total_messages"] == 2
    assert final_stats["users"] == {"user1": 2}
    assert final_stats["hourly_distribution"] == {"14": 2}
    assert final_stats["daily_distribution"] == {"Viernes": 2}
    assert final_stats["top_words"] == [("gracias", 2)]
