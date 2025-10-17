import requests
import aiohttp
import asyncio

async def descargar_async():
    # # requests.get() NO es awaitable, bloquea el thread
    # response = await requests.get("https://www.promiedos.com.ar")  # ✗ Error
    
    # aiohttp.get() SÍ es awaitable, no bloquea
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.promiedos.com.ar/") as response:  # ✓ Correcto
            return await response.text()
        
async def main():
    print(await descargar_async())
    
if __name__ == "__main__":
    asyncio.run(main())