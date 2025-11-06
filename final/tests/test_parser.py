from datetime import datetime
from src.worker.parser import parse_whatsapp_line, extract_stats_from_subchunk


def test_parse_whatsapp_line_valid():
    """Test parsing of a valid message line."""
    line = (
        "27/03/2024, 09:17 - Julián (Soporte): Estamos ajustando la carga del servidor."
    )
    data = parse_whatsapp_line(line)
    assert data is not None
    assert data["date"] == datetime(2024, 3, 27)
    assert data["hour"] == "09"
    assert data["day_of_week"] == "Miércoles"
    assert data["user"] == "Julián (Soporte)"
    assert data["message"] == "estamos ajustando la carga del servidor."


def test_parse_whatsapp_line_invalid():
    """Test that system messages or invalid lines return None."""
    line = "27/03/2024, 08:12 - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them."
    data = parse_whatsapp_line(line)
    assert data is None


def test_parse_whatsapp_line_invalid_date():
    """Test that lines with invalid dates return None."""
    line = "30/02/2024, 09:17 - Julián (Soporte): Esto no se debería parsear."
    data = parse_whatsapp_line(line)
    assert data is None


def test_extract_stats_from_subchunk():
    """Test stats extraction from a list of lines, including invalid ones."""
    lines_list = [
        "27/03/2024, 08:12 - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.",
        "27/03/2024, 09:17 - Julián (Soporte): Estamos ajustando la carga del servidor. Te aviso cuando normalice.",
        "27/03/2024, 11:02 - +54 9 11 3987-1951: El sistema me desconecta cada 10 minutos.",
        "Esto es una línea que no matchea con el regex",
        "28/03/2024, 11:05 - Julián (Soporte): Problema resuelto.",
    ]
    result = extract_stats_from_subchunk(lines_list)

    # Should only process the 3 valid messages
    assert result["total_messages"] == 3

    # Check total message length
    # len("estamos ajustando la carga del servidor. te aviso cuando normalice.") = 67
    # len("el sistema me desconecta cada 10 minutos.") = 41
    # len("problema resuelto.") = 18
    # Total = 67 + 41 + 18 = 126
    assert result["total_message_length"] == 126

    # Check user stats
    assert len(result["users"]) == 2
    assert result["users"]["Julián (Soporte)"] == 2
    assert result["users"]["+54 9 11 3987-1951"] == 1

    # Check hourly distribution
    assert result["hourly_distribution"]["09"] == 1
    assert result["hourly_distribution"]["11"] == 2

    # Check daily distribution
    assert result["daily_distribution"]["Miércoles"] == 2
    assert result["daily_distribution"]["Jueves"] == 1

    # Check top words (basic check)
    assert result["top_words"]["servidor"] == 1
    assert result["top_words"]["problema"] == 1
