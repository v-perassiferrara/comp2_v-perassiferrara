def split_list_into_chunks(data_list: list, chunk_size: int) -> list[list]:
    """
    Toma una lista y la devuelve en pedazos de 'chunk_size'.
    """
    if not data_list:
        return []
    return [data_list[i : i + chunk_size] for i in range(0, len(data_list), chunk_size)]


# Constantes de Red
DEFAULT_HOST = "::"  # Escucha en IPv4 y IPv6, para permitir dual-stack
DEFAULT_PORT = 8888
