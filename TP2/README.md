# TP2 - Sistema de Scraping y Análisis Web Distribuido

Este proyecto implementa un sistema distribuido para scraping y análisis de páginas web, compuesto por dos servidores: uno de extracción asíncrono (Server A) y otro de procesamiento con multiprocessing (Server B).

## Estructura del Proyecto

```
TP2/
├── server_scraping.py          # Servidor asyncio (Parte A)
├── server_processing.py        # Servidor multiprocessing (Parte B)
├── client.py                   # Cliente de prueba
├── scraper/
│   ├── __init__.py
│   ├── html_parser.py          # Funciones de parsing HTML
│   ├── metadata_extractor.py  # Extracción de metadatos
│   └── async_http.py           # Cliente HTTP asíncrono
├── processor/
│   ├── __init__.py
│   ├── screenshot.py           # Generación de screenshots
│   ├── performance.py          # Análisis de rendimiento
│   └── image_processor.py      # Procesamiento de imágenes
├── common/
│   ├── __init__.py
│   ├── protocol.py             # Protocolo de comunicación
│   └── serialization.py        # Serialización de datos
├── requirements.txt
└── README.md
```

## Instalación

1.  Clonar el repositorio:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd TP2
    ```

2.  Crear un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv venv
    ./venv/Scripts/activate  # En Windows
    # source venv/bin/activate # En Linux/macOS
    ```

3.  Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4.  Instalar los navegadores para Playwright (necesario para screenshots y análisis de rendimiento):
    ```bash
    playwright install
    ```

## Uso

### 1. Iniciar el Servidor de Procesamiento (Parte B)

Este servidor debe iniciarse primero. Escucha en un puerto específico y utiliza un pool de procesos para tareas intensivas.

```bash
python server_processing.py -i 127.0.0.1 -p 8001 -n 4
```

Opciones:
-   `-i IP, --ip IP`: Dirección de escucha (ej. `127.0.0.1`)
-   `-p PORT, --port PORT`: Puerto de escucha (ej. `8001`)
-   `-n PROCESSES, --processes PROCESSES`: Número de procesos en el pool (por defecto: CPU count)

### 2. Iniciar el Servidor de Scraping (Parte A)

Este servidor HTTP asíncrono recibe las solicitudes del cliente, realiza el scraping y coordina con el Servidor de Procesamiento.

```bash
python server_scraping.py -i 127.0.0.1 -p 8000 -w 4
```

Opciones:
-   `-i IP, --ip IP`: Dirección de escucha (soporta IPv4/IPv6, ej. `127.0.0.1`)
-   `-p PORT, --port PORT`: Puerto de escucha (ej. `8000`)
-   `-w WORKERS, --workers WORKERS`: Número de workers (por defecto: `4`)

### 3. Ejecutar el Cliente de Prueba

El cliente interactúa con el Servidor de Scraping para solicitar el análisis de una URL.

```bash
python client.py --url https://www.google.com
```

Opciones:
-   `--url URL`: URL a scrapear y analizar.

## Formato de Respuesta

El servidor de scraping devolverá una respuesta JSON con la siguiente estructura:

```json
{
  "url": "https://ejemplo.com",
  "timestamp": "2024-11-10T15:30:00Z",
  "scraping_data": {
    "title": "Título de la página",
    "links": ["url1", "url2", "..."],
    "meta_tags": {
      "description": "...",
      "keywords": "...",
      "og:title": "..."
    },
    "structure": {
      "h1": 2,
      "h2": 5,
      "h3": 10
    },
    "images_count": 15
  },
  "processing_data": {
    "screenshot": "base64_encoded_image",
    "performance": {
      "load_time_ms": 1250,
      "total_size_kb": 2048,
      "num_requests": 45
    },
    "thumbnails": ["base64_thumb1", "base64_thumb2"]
  },
  "status": "success"
}
```
