# Instalación y Ejecución

El proyecto está diseñado para ejecutarse con Docker Compose, que gestiona el _backend_ (Servidor, 4 Workers y Redis). El Cliente se ejecuta localmente para conectarse al sistema.

## 1. Prerrequisitos

- **Docker y Docker Compose:** Necesarios para levantar el _backend_.
- **Python 3.10+:** Necesario para correr el _cliente_ local.

## 2. Preparar el Entorno Local (para el Cliente)

(Opcional pero recomendado) Crea un entorno virtual para ejecutar el cliente.

```bash
# 1. Crear el entorno (en la raíz del proyecto)
python3 -m venv venv

# 2. Activar el entorno
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## 3\. Ejecutar el Sistema

Se necesitan **dos terminales**: una para el _Backend_ (Docker) y otra para el _Cliente_ (Local).

### Terminal 1: Backend (Servidor + Workers + Redis)

Navega a la carpeta `docker/` y levanta todos los servicios.

```bash
# Navegar a la carpeta docker
cd docker

# Levantar todo (y reconstruir si hay cambios)
docker-compose up --build
```

> Deja esta terminal abierta. Verás los logs de los 6 contenedores (1 Server, 1 Redis, 4 Workers).

---

### Terminal 2: Cliente (Local)

En **otra terminal** (con tu `venv` activado), párate en la **raíz del proyecto** (`.../final/`) y ejecuta el cliente:

```bash
# (Asegúrate de estar en .../final/ y tener el venv activado)
python -m src.client.client whatsapp_support_chat.txt
```

> _[Para analizar otro archivo, cambiar la ruta en el argumento del cliente por la ruta al archivo de chat deseado]_.
