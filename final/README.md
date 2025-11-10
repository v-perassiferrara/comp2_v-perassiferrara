# Sistema Distribuido de Análisis de Chats

> Trabajo realizado por: Valentino Perassi Ferrara. Legajo: 63252. Año: 2025.

El presente repositorio contiene el código del proyecto final de la materia Computación II, siendo este un sistema cliente-servidor para análisis de chats de WhatsApp Business exportados, orientado a métricas operativas de equipos de soporte empresarial.

Utiliza una **arquitectura híbrida**: Celery para distribución entre workers y `multiprocessing.Pool` para paralelismo local en cada worker.

---

## 🚀 Instalación y Ejecución

Las instrucciones completas para la instalación y el despliegue con Docker se encuentran en: **[INSTALL.md](./INSTALL.md)**

---

## 💻 Ayuda del Cliente

El sistema se utiliza a través del `client.py`:

```bash
usage: python -m src.client.client [-h] [--host HOST] [--port PORT] filepath
```

#### Argumentos Posicionales

- `filepath`: Ruta al archivo de chat (.txt) a procesar.

#### Opcionales

- `-h, --help`: Muestra el mensaje de ayuda y sale.
- `--host HOST`: Host del servidor (default: `::`, dual-stack).
- `--port PORT`: Puerto del servidor (default: `8888`).
