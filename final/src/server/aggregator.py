from collections import Counter


def aggregate_final_stats(results_list):
    total_users = Counter()
    total_hourly = Counter()
    total_daily = Counter()
    total_words = Counter()
    total_messages = 0
    total_message_length = 0

    for result in results_list:
        if result:
            total_messages += result.get("total_messages", 0)
            total_message_length += result.get("total_message_length", 0)

            total_users.update(result.get("users", {}))
            total_hourly.update(result.get("hourly_distribution", {}))
            total_daily.update(result.get("daily_distribution", {}))

            words_dict = dict(result.get("top_words", []))
            total_words.update(words_dict)

    # Cálculo final
    average_length = 0
    if total_messages > 0:
        average_length = round(total_message_length / total_messages, 2)

    return {
        "total_messages": total_messages,
        "average_message_length": average_length,
        "users": dict(total_users),
        "hourly_distribution": dict(total_hourly),
        "daily_distribution": dict(total_daily),
        "top_words": total_words.most_common(10),
        "workers_used": len(results_list),
    }
