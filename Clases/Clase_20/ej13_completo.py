import asyncio
import aiohttp

# Generador para producir URLs
def generar_urls(base, cantidad):
    """Generador clásico: produce URLs sin cargarlas todas en memoria"""
    for i in range(1, cantidad + 1):
        yield f"{base}/page/{i}"

# Corrutina para descargar una URL
async def descargar(session, url):
    """Corrutina asíncrona: descarga sin bloquear"""
    async with session.get(url) as response:
        contenido = await response.text()
        return len(contenido)

# Orquestador principal
async def main():
    urls = generar_urls("http://example.com", 50)
    
    async with aiohttp.ClientSession() as session:
        # Crear tareas para todas las URLs
        tareas = [descargar(session, url) for url in urls]
        
        # Ejecutar todas concurrentemente
        resultados = await asyncio.gather(*tareas)
        
        total = sum(resultados)
        print(f"Descargadas {len(resultados)} páginas")
        print(f"Total de bytes: {total:,}")

asyncio.run(main())