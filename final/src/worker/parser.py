import re
from collections import Counter
from datetime import datetime


# Palabras que no se agregan a la lista de más frecuentes
STOPWORDS = set(
    [
        "de",
        "la",
        "que",
        "el",
        "en",
        "y",
        "a",
        "los",
        "del",
        "con",
        "un",
        "una",
        "por",
        "para",
        "no",
        "se",
        "mi",
        "me",
        "te",
        "q",
        "es",
        "al",
        "si",
        "ya",
        "hola",
        "buenos",
        "días",
        "como",
        "puedo",
        "ayudarte",
        "claro",
        "dime",
        "cual",
        "tu",
        "le",
        "<media",
        "media",
        "omitted",
        "omitted>",
        "link",
        "importante",
        "http",
        "httpss",
        "www",
        "eso",
        "estamos",
        "cuando",
        "cada",
        "te",
        "necesito",
        "podés",
        "tecnosoft",
        "soporte",
        "aviso",
        "cuando",
        "normalice",
    ]
)

WEEK_DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def parse_whatsapp_line(line):
    """
    Parsea una línea de WhatsApp exportado.
    Formato: DD/MM/YYYY, HH:MM - Usuario: Mensaje
    """

    # Regex para extraer fecha/hora, usuario y mensaje
    pattern = r"(\d{1,2}/\d{1,2}/\d{4}), (\d{1,2}:\d{2}) - ([^:]+): (.+)"
    match = re.match(pattern, line)

    if not match:
        return None

    try:
        # Strptime para validar y convertir a datetime
        date_object = datetime.strptime(match.group(1), "%d/%m/%Y")

        # Si es correcto, devuelve un diccionario con la información extraída: fecha, hora, día, usuario y mensaje
        return {
            "date": date_object,
            "hour": match.group(2)
            .split(":")[0]
            .zfill(2),  # Formato de 2 dígitos, por ejemplo: 8:00 -> 08:00
            "day_of_week": WEEK_DAYS[date_object.weekday()],  # "Lunes", "Martes", ...
            "user": match.group(3).strip(),
            "message": match.group(4).strip().lower(),
        }

    except ValueError:
        # Fecha inválida (ej. 30/02/2020)
        return None


def extract_stats_from_subchunk(lines_list):
    """
    Función principal de un subproceso llamada por el ProcessPoolExecutor.
    Recibe un sub-chunk (lista de strings) y devuelve un diccionario de estadísticas parciales.
    """

    # Contadores de usuarios, horas, días, palabras, mensajes
    # Un counter cuenta la frecuencia de múltiples elementos únicos
    users = Counter()
    hourly_dist = Counter()
    daily_dist = Counter()
    top_words = Counter()
    total_msgs = 0
    total_msg_length = 0

    for line in lines_list:
        data = parse_whatsapp_line(line)

        if data:
            total_msgs += 1
            total_msg_length += len(data["message"])
            users[data["user"]] += 1
            hourly_dist[data["hour"]] += 1
            daily_dist[data["day_of_week"]] += 1

            # Limpiar links y procesar palabras
            message_no_links = re.sub(r"https?://\S+|www\.\S+", " ", data["message"])
            words = re.findall(r"\b\w{4,}\b", message_no_links)
            for word in words:
                if word not in STOPWORDS:
                    top_words[word] += 1

    # Devolvemos el "JSON parcial del sub-chunk" como un diccionario
    return {
        "total_messages": total_msgs,
        "total_message_length": total_msg_length,
        "users": users,
        "hourly_distribution": hourly_dist,
        "daily_distribution": daily_dist,
        "top_words": top_words,
    }
