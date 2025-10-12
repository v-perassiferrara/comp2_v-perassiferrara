import asyncio

# Esto es una corrutina
async def mi_primera_corrutina():
    print("Iniciando...")
    await asyncio.sleep(1)  # Pausa por 1 segundo
    print("¡Terminé!")

# Para ejecutarla necesitamos un event loop
asyncio.run(mi_primera_corrutina())