import asyncio


# Internamente, gather() crea tasks (tareas) para cada corrutina
# y le dice al event loop: "Ejecuta todas estas, y avísame cuando todas terminen".



async def tarea_a():
    await asyncio.sleep(2)
    return "A terminó"

async def tarea_b():
    await asyncio.sleep(1)
    return "B terminó"

async def main():
    # Sin gather (secuencial)
    resultado_a = await tarea_a()  # Espera 2s           # noqa: F841
    resultado_b = await tarea_b()  # Espera 1s más       # noqa: F841
    # Total: 3s
    
    # Con gather (concurrente)
    resultados = await asyncio.gather(
        tarea_a(),  # Empieza
        tarea_b()   # Empieza casi al mismo tiempo
    )
    # Total: 2s (el máximo de ambas)
    print(resultados)  # ["A terminó", "B terminó"]