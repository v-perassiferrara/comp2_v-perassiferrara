# Usar una imagen base de Alpine, que es súper ligera
FROM python:alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el script del servidor
COPY server.py .

# Comando de ejecución (sin cambios)
CMD ["python", "-u", "server.py"]