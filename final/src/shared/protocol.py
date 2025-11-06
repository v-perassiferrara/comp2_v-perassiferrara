from typing import TypedDict, Counter

# Estructura de las estadísticas parciales generadas por cada sub-proceso
class PartialStats(TypedDict):
    total_messages: int
    users: Counter[str]
    hourly_distribution: Counter[str]
    daily_distribution: Counter[str]
    top_words: Counter[str]
