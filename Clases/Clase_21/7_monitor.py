import asyncio
import aiohttp
from datetime import datetime

'''
Objetivo: Crear un programa que monitoree el estado de múltiples sitios web cada 30 segundos.

Requisitos:

    Mantener una lista de URLs a monitorear
    Cada 30 segundos, verificar todas las URLs concurrentemente
    Registrar el tiempo de respuesta y código de estado
    Si un sitio falla 3 veces consecutivas, mostrar una alerta
    El programa debe correr indefinidamente hasta Ctrl+C

Pistas:

    Usa asyncio.sleep(30) en un loop infinito
    Mantén un diccionario de contadores de fallos por URL
    asyncio.create_task() para no bloquear el monitoreo

'''

TIEMPO_ENTRE_INTENTOS = 6   # deberia ser 30, pero para facilidad de depuración uso menos


async def revisar_sitio(session, url, fallos):
    while True:
        inicio = datetime.now()
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    print(f"✅ {url}: OK")
                    fallos[url]["error"] = 0 # para que la alerta solo aparezca si falla 3 veces consecutivas
                    fallos[url]["timeout"] = 0 
                else:
                    print(f"❌ {url}: Fallo {response.status}")
                    fallos[url]["error"] += 1
                    
                    if fallos[url]["error"] >= 3:
                        print(f"❌ {url}: Alerta de fallo excesivo")
                
        except asyncio.TimeoutError:    # la misma logica para timeout
            print(f"⏱️ {url}: Timeout")
            fallos[url]["timeout"] += 1
            
            if fallos[url]["timeout"] >= 3:
                print(f"❌ {url}: Alerta de timeout excesivo")
        
        duracion = (datetime.now() - inicio).total_seconds()    # calculamos tiempo de respuesta
        print(f"  Tiempo de respuesta de {url}: {duracion:.2f}s\n")

        print(f"  ⏳ Esperando {TIEMPO_ENTRE_INTENTOS}s...\n")
        await asyncio.sleep(TIEMPO_ENTRE_INTENTOS)  # se "pausa" entre iteraciones



async def monitorear_sitios(urls):
    
    async with aiohttp.ClientSession() as session:
        fallos = {url: {"error": 0, "timeout": 0} for url in urls}
        
        
        tareas = [asyncio.create_task(revisar_sitio(session, url, fallos)) for url in urls]
        
        
        while True:
            await asyncio.gather(*tareas)

async def main():
    sitios = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.python.org",
        "https://www.wikipedia.org",
        "https://um.edu.ar"
    ]
    await monitorear_sitios(sitios)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nPrograma detenido por el usuario.")
