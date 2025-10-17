import asyncio
import time


async def mi_corrutina():
    return 42

# Esto es un awaitable (es una corrutina)
resultado = await mi_corrutina()  # SOLO FUNCIONA DENTRO DE UNA FUNCION ASYNC (corrutina), excepto en IPython

# Esto NO es awaitable

await time.sleep(1)  # ✗ TypeError: object float can't be used in 'await' expression