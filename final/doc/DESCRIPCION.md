# Sistema Distribuido de Análisis de Chats

## Descripción

Sistema cliente-servidor para análisis de chats de WhatsApp Business exportados, orientado a métricas operativas de equipos de soporte empresarial. Utiliza **arquitectura híbrida**: Celery para distribución entre workers y multiprocessing.Pool para paralelismo local en cada worker.

**Caso de uso:** Empresas con soporte vía WhatsApp procesan miles de consultas diarias. Analizar manualmente archivos de meses resultaría muy lento y engorroso. Este sistema reduce drásticamente este tiempo mediante procesamiento distribuido y paralelo, extrayendo métricas de carga por agente, horarios pico y problemas recurrentes.

**Flujo:**

1. Cliente envía archivo .txt vía TCP (IPv4/IPv6)
2. Servidor asyncio divide en 4 chunks grandes y despacha tareas a Redis
3. Workers Celery procesan chunks en paralelo (cada uno usa Pool local de 4 procesos)
4. Workers consolidan resultados parciales y los guardan en Redis
5. Servidor agrega resultados finales y responde JSON al cliente

**Concurrencia:** Servidor asyncio maneja múltiples clientes simultáneamente, cada uno con su propio conjunto de workers procesando en paralelo.

**IPC:**

- **Distribuido:** Redis Queue (broker Celery) + Result Backend
- **Local:** multiprocessing.Queue y Value dentro de cada worker para coordinar su Pool

**Paralelismo multinivel:**

- Nivel 1: Celery distribuye 4 chunks a workers (diferentes máquinas potenciales)
- Nivel 2: Cada worker subdivide su chunk en ~25 sub-chunks procesados por Pool(4)

## Arquitectura

```
Cliente TCP ──→ Servidor asyncio ──→ Redis ──→ 4 Workers Celery
                     ↑                            │ (cada uno con Pool local)
                     │                            │
                     └────── Redis Backend ←──────┘
                  (espera de resultados + agregación)
```

## Componentes

**Cliente:** argparse + socket TCP → envía archivo → recibe JSON

**Servidor:** asyncio + dual-stack → divide archivo → despacha tareas → espera resultados de Redis → agrega resultados

**Workers:** Reciben chunk → crean Queue/Value locales → lanzan Pool(4) → sub-procesos parsean regex → consolidan → retornan

**Redis:** Broker de tareas + almacenamiento de resultados consolidados

## Estadísticas Extraídas

- Total de mensajes
- Mensajes por usuario (empleado/agente)
- Palabras clave (más usadas)
- Distribución horaria/semanal
- Longitud promedio de mensajes
- Tiempo de ejecución

## Tecnologías

- Python 3.10+
- asyncio
- Celery
- Redis
- multiprocessing.Pool
- socket IPv4/IPv6
- argparse
- Docker

## Justificaciones Técnicas

**¿Por qué híbrido (Celery + Pool)?**

- Celery: escala horizontalmente entre máquinas
- Pool: aprovecha cores locales
- Balance óptimo: distribución + paralelismo

**¿Por qué chunks grandes → sub-chunks?**

- Minimiza overhead de serialización Redis (4 tareas grandes vs 100 pequeñas)
- Cada worker subdivide localmente para paralelismo CPU

**¿Por qué asyncio en servidor?**

- Servidor es I/O-bound (sockets + espera de Redis)
- Workers son CPU-bound (parseo regex en Pool)
