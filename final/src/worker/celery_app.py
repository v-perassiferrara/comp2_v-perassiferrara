from celery import Celery

# Usaremos Redis como broker y result_backend.

# El broker es quien se encarga de enviar las tareas a los workers.
# El backend es donde se almacenan los resultados de las tareas.

# 'include' es una lista de módulos que se importarán cuando el worker inicie.
app = Celery(
    "worker",
    # Para probar en local
    # broker="redis://localhost:6379/0",
    # backend="redis://localhost:6379/1",
    # Para usar con Docker
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
    include=["src.worker.tasks"],
)

# Configuración para usar JSON en la serialización.
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Argentina/Mendoza",
    enable_utc=True,
)
