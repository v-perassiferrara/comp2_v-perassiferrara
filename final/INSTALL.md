# Instalación y Ejecución

> Local (Sin Docker)

### 1. Entorno Virtual (Opcional)

Crear un entorno virtual:

```bash
python3 -m venv venv
```

---

Activar el entorno virtual:

```bash
source venv/bin/activate
```

---

Instalar dependencias:

```bash
pip install -r requirements.txt
```

### 2. Ejecución

Abrir 4 terminales separadas en la raíz del proyecto (`.../final/`).

---

### Terminal 1: Redis

```bash
docker run -d -p 6379:6379 redis:alpine
```

---

### Terminal 2: Worker (Celery)

```bash
PYTHONPATH=. celery -A src.worker.celery_app worker --loglevel=info --pool=threads
```

---

### Terminal 3: Server (Asyncio)

```bash
python -m src.server.server
```

---

### Terminal 4: Cliente

```bash
python -m src.client.client tests/sample_chat.txt
```

> _Para analizar otro archivo, cambiar la ruta en el argumento del cliente por la ruta al archivo de chat deseado_.
