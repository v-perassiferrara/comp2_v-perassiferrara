# Etapa 1: Simula leer líneas de un archivo grande
def lector_logs():
    logs = [
        "2024-10-06 10:23:45 ERROR Database connection failed",
        "2024-10-06 10:23:46 INFO User login: john@example.com",
        "2024-10-06 10:23:47 ERROR Null pointer exception",
        "2024-10-06 10:23:48 WARNING Low memory: 85% used",
        "2024-10-06 10:23:49 INFO User logout: mary@example.com",
    ]
    for linea in logs:
        yield linea

# Etapa 2: Extrae solo errores
def filtro_errores(lineas):
    for linea in lineas:
        if "ERROR" in linea:
            yield linea

# Etapa 3: Extrae el mensaje limpio
def extraer_mensaje(lineas):
    for linea in lineas:
        # Quita la fecha y el nivel de log
        partes = linea.split(maxsplit=3)
        if len(partes) >= 4:
            yield partes[3]

# Construyendo el pipeline
logs = lector_logs()
errores = filtro_errores(logs)
mensajes = extraer_mensaje(errores)

# Ahora procesamos
for mensaje in mensajes:
    print(f"⚠️  {mensaje}")