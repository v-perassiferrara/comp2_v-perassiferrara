# Usar la misma imagen base de Alpine
FROM python:alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el script del cliente
COPY cliente.py .

# Comando de ejecución (sin cambios)
CMD ["python", "-u", "cliente.py"]