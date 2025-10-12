# versión con archivo real de dpkg.log



# Etapa 1: Leer líneas de un archivo grande

def lector_logs():  
    with open("/var/log/dpkg.log","r") as logs_file:
        for linea in logs_file:
            yield linea.strip()

# Etapa 2: Extrae solo installs
def filtro_installs(lineas):
    for linea in lineas:
        if "install" in linea:
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
installs = filtro_installs(logs)
mensajes = extraer_mensaje(installs)

# Ahora procesamos
for mensaje in mensajes:
    print(f"⚠️  {mensaje}")