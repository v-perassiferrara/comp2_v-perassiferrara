def split_list_into_chunks(data_list: list, chunk_size: int) -> list[list]:
    """
    Toma una lista y la devuelve en pedazos de 'chunk_size' (lista de listas de tamaño 'chunk_size').
    """
    if not data_list:
        return []
    return [data_list[i : i + chunk_size] for i in range(0, len(data_list), chunk_size)]


# Constantes de Red
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8888
BUFFER_SIZE = 4096

# Constantes de Workers y Procesamiento
PROCESSING_WORKERS = 4
RESULTS_TIMEOUT = 120
SUB_CHUNK_SIZE = 1000

# Constantes de Parseo de WhatsApp
WEEK_DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
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
