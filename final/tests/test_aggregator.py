from src.server.aggregator import aggregate_final_stats


def test_aggregate_final_stats_basic():
    """Test aggregation with two valid worker results."""
    results_list = [
        {
            "total_messages": 3,
            "total_message_length": 50,
            "users": {"user1": 2, "user2": 1},
            "hourly_distribution": {"09": 2, "10": 1},
            "daily_distribution": {"Lunes": 2, "Martes": 1},
            "top_words": [("hola", 4), ("mundo", 2)],
        },
        {
            "total_messages": 2,
            "total_message_length": 30,
            "users": {"user1": 1, "user3": 1},
            "hourly_distribution": {"10": 1, "11": 1},
            "daily_distribution": {"Martes": 2},
            "top_words": [("adios", 1), ("gracias", 1)],
        },
    ]
    final_stats = aggregate_final_stats(results_list)
    assert final_stats["total_messages"] == 5
    assert final_stats["average_message_length"] == 16.0
    assert final_stats["users"] == {"user1": 3, "user2": 1, "user3": 1}
    assert final_stats["hourly_distribution"] == {"09": 2, "10": 2, "11": 1}
    assert final_stats["daily_distribution"] == {"Lunes": 2, "Martes": 3}
    assert final_stats["top_words"] == {
        "hola": 4,
        "mundo": 2,
        "adios": 1,
        "gracias": 1,
    }
    assert final_stats["workers_used"] == 2


def test_aggregate_final_stats_with_failed_workers():
    """Test that aggregation handles empty or None results gracefully."""
    worker_results = [
        {
            "total_messages": 10,
            "total_message_length": 200,
            "users": {"user1": 10},
            "hourly_distribution": {"09": 10},
            "daily_distribution": {"Lunes": 10},
            "top_words": [("test", 10)],
        },
        None,
        {},
    ]
    final_stats = aggregate_final_stats(worker_results)
    assert final_stats["total_messages"] == 10
    assert final_stats["average_message_length"] == 20.0
    assert final_stats["users"] == {"user1": 10}
    assert final_stats["hourly_distribution"] == {"09": 10}
    assert final_stats["daily_distribution"] == {"Lunes": 10}
    assert final_stats["top_words"] == {"test": 10}
    assert final_stats["workers_used"] == 3


def test_aggregate_final_stats_empty_input():
    """Test aggregation with an empty list of results."""
    final_stats = aggregate_final_stats([])
    assert final_stats["total_messages"] == 0
    assert final_stats["average_message_length"] == 0
    assert final_stats["users"] == {}
    assert final_stats["hourly_distribution"] == {}
    assert final_stats["daily_distribution"] == {}
    assert final_stats["top_words"] == {}
    assert final_stats["workers_used"] == 0


def test_aggregate_final_stats_zero_messages():
    """Test division-by-zero protection when total_messages is 0."""
    worker_results = [
        {
            "total_messages": 0,
            "total_message_length": 0,
            "users": {},
            "hourly_distribution": {},
            "daily_distribution": {},
            "top_words": [],
        },
    ]
    final_stats = aggregate_final_stats(worker_results)
    assert final_stats["total_messages"] == 0
    assert final_stats["average_message_length"] == 0
    assert final_stats["users"] == {}
    assert final_stats["hourly_distribution"] == {}
    assert final_stats["daily_distribution"] == {}
    assert final_stats["top_words"] == {}
    assert final_stats["workers_used"] == 1
