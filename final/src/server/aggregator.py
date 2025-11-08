from collections import Counter

# Para ordenar los días de la semana
WEEK_DAYS_ORDER = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo",
]


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

    # Mejoras de formato para la salida final

    # Filtrar y ordenar usuarios (no incluir números desconocidos, solo empleados)
    employee_users_counter = Counter(
        {user: count for user, count in total_users.items() if "+" not in user}
    )
    sorted_employee_users = dict(employee_users_counter.most_common())

    # Ordenar dias de la semana usando la lista como clave
    sorted_daily = dict(
        sorted(total_daily.items(), key=lambda item: WEEK_DAYS_ORDER.index(item[0]))
    )

    # Ordenar horas del dia
    sorted_hourly = dict(sorted(total_hourly.items()))

    # Formato de top words

    return {
        "total_messages": total_messages,
        "average_message_length": average_length,
        "users": sorted_employee_users,
        "hourly_distribution": sorted_hourly,  # Versión ordenada
        "daily_distribution": sorted_daily,  # Versión ordenada
        "top_words": dict(total_words.most_common(10)),
        "workers_used": len(results_list),
    }
