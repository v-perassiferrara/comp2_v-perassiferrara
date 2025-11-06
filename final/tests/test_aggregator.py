from src.server.aggregator import aggregate_final_stats


def test_aggregate_final_stats():
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
    assert final_stats["average_message_length"] == 16
    assert final_stats["users"] == {"user1": 3, "user2": 1, "user3": 1}
    assert final_stats["hourly_distribution"] == {"09": 2, "10": 2, "11": 1}
    assert final_stats["daily_distribution"] == {"Lunes": 2, "Martes": 3}
    top_words_dict = dict(final_stats["top_words"])
    assert top_words_dict["hola"] == 4
    assert top_words_dict["mundo"] == 2
    assert top_words_dict["adios"] == 1
    assert top_words_dict["gracias"] == 1
