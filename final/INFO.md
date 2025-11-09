# Información Técnica: Decisiones de Diseño

Este documento resume las principales decisiones de diseño y arquitectura del "Sistema Distribuido de Análisis de Chats", justificando el porqué de cada tecnología seleccionada.

## 1. Arquitectura Híbrida (Celery + Multiprocessing)

La decisión principal fue adoptar una arquitectura híbrida en lugar de usar solo Celery o solo `multiprocessing`.

- **¿Por qué no solo Celery?** Despachar miles de tareas pequeñas (una por cada línea de chat) generaría un _overhead_ inmenso en la red y en el _broker_ (Redis).
- **¿Por qué no solo `multiprocessing`?** Un solo `Pool` en el servidor no escala. Limitaría el procesamiento a los núcleos de una sola máquina (el servidor), creando un cuello de botella.

- **Solución (Híbrida):** El servidor divide el trabajo en 4 _chunks_ grandes y los distribuye con **Celery** (que puede escalar incluso a otras máquinas). Luego, cada _worker_ de Celery, que es CPU-bound (Regex y conteo de estadísticas), usa un **`multiprocessing.Pool`** local para paralelizar el procesamiento de su _chunk_ asignado usando todos sus núcleos. Esto nos da lo mejor de ambos mundos: **distribución** (Celery) y **paralelismo** (Pool).

---

## 2. Servidor `asyncio` (Asincronismo I/O)

El servidor principal (`server.py`) se construyó con `asyncio` en lugar de un servidor de _sockets_ tradicional (ej. con hilos).

- **Justificación:** El servidor es **I/O-bound** (limitado por E/S), no por CPU. Sus tareas principales son:
  1.  Esperar conexiones de red (`await reader.read()`).
  2.  Esperar los resultados de Celery (`await asyncio.sleep(1.0)`).
- `asyncio` es la herramienta perfecta para esto. Permite al servidor manejar **cientos de clientes concurrentes** en un solo hilo (el _event loop_), cediendo el control eficientemente durante los tiempos de espera (como el _polling_ de Redis) en lugar de bloquear un hilo por cada cliente.

---

## 3. Gestión de Procesos en Workers

La implementación del _worker_ (`tasks.py`) fue la parte más compleja. El objetivo era anidar un `multiprocessing.Pool` (CPU-bound) dentro de un _worker_ de Celery (I/O-bound). Esto requirió 4 soluciones específicas para resolver conflictos de bajo nivel:

1.  **`--pool=threads` (en Celery):** El _pool_ por defecto de Celery (`prefork`) usa procesos _daemonic_. Python **prohíbe** que un proceso _daemonic_ cree procesos hijos (nuestro `Pool`), causando un `AssertionError`. La solución fue correr el _worker_ de Celery en modo hilos.

2.  **`Manager()` (en `tasks.py`):** Un _hilo_ (el _worker_) no puede "heredar" objetos de IPC (como una `Queue` cruda) a un `Pool` de procesos. Esto causaba un `RuntimeError`. La solución fue usar `multiprocessing.Manager()`, que crea la `Queue` y el `Value` en un proceso "servidor" separado, permitiendo que tanto el _hilo_ como los _procesos_ del `Pool` se comuniquen con él a través de _proxies_.

3.  **`get_context("spawn")` (en `tasks.py`):** A pesar de usar `Manager`, la comunicación fallaba con `[Errno 2]` porque el método `fork` por defecto heredaba mal el estado del _hilo_. Forzar el contexto a `"spawn"` garantiza que cada proceso del `Pool` arranque "limpio", resolviendo los conflictos de IPC.

4.  **`PYTHONPATH=.` (en Terminal):** Al usar `"spawn"`, los procesos hijos nacen "sueltos/vírgenes" y no saben dónde está el módulo `src`. Añadir la raíz del proyecto al `PYTHONPATH` asegura que puedan encontrar los módulos de `parser`, `consolidator`, etc.

---

## 4. Doble Mecanismo de IPC

Con esto, el proyecto usa dos niveles de IPC intencionadamente:

- **IPC Distribuida (Redis):** Se usa para la comunicación entre el _Servidor_ y los _Workers_. Es robusta, en red y asincrónica, gestionada por Celery.

- **IPC Local (`Manager().Queue()`):** Se usa para la comunicación _dentro_ de un solo _Worker_, entre el hilo principal y su `Pool` de procesos hijos. Es local y efímera.
