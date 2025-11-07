from collections import Counter


def consolidate_results(result_queue, total_sub_chunks):
    """
    Recolecta y consolida los resultados de todos los sub-procesos.
    Espera hasta que se hayan procesado todos los sub-chunks.
    Tras consolidar, retorna el diccionario final de resultados (del chunk "grande").
    """
    # Contadores totales para todas las estadísticas
    total_users = Counter()
    total_hourly = Counter()
    total_daily = Counter()
    total_words = Counter()
    total_messages = 0
    total_message_length = 0

    processed_sub_chunks = 0
    while processed_sub_chunks < total_sub_chunks:
        try:
            # Espera bloqueante hasta que un resultado esté disponible
            result = result_queue.get()
            if result:
                total_messages += result.get("total_messages", 0)
                total_message_length += result.get("total_message_length", 0)
                total_users.update(result.get("users", {}))
                total_hourly.update(result.get("hourly_distribution", {}))
                total_daily.update(result.get("daily_distribution", {}))
                total_words.update(result.get("top_words", {}))
            processed_sub_chunks += 1
        except Exception as e:
            # Manejar posible error en la cola o en los datos
            print(f"Error consolidando resultado: {e}")
            processed_sub_chunks += 1  # Asegurarse de no quedar en un bucle infinito

    # Devuelve el diccionario consolidado final
    return {
        "total_messages": total_messages,
        "total_message_length": total_message_length,
        "users": dict(total_users),
        "hourly_distribution": dict(total_hourly),
        "daily_distribution": dict(total_daily),
        "top_words": total_words.most_common(10),  # Top 10 palabras más comunes
    }
