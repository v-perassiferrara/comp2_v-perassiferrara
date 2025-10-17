import asyncio
import aiohttp
import random

async def fetch_con_retry(session, url, max_intentos=3, backoff_base=1):
    """
    Intenta fetch con reintentos exponenciales
    
    Args:
        session: ClientSession de aiohttp
        url: URL a descargar
        max_intentos: Número máximo de intentos
        backoff_base: Segundos base para backoff (se duplica cada intento)
    """
    for intento in range(1, max_intentos + 1):
        try:
            print(f"  🔄 Intento {intento}/{max_intentos} para {url}")
            
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    contenido = await response.text()
                    print(f"  ✅ Éxito en intento {intento}")
                    return contenido
                
                elif response.status >= 500:
                    # Error del servidor, vale la pena reintentar
                    print(f"  ⚠️  Error {response.status}, reintentando...")
                    
                else:
                    # Error del cliente (4xx), no vale la pena reintentar
                    print(f"  ❌ Error {response.status}, no reintentable")
                    return None
        
        except asyncio.TimeoutError:
            print(f"  ⏱️  Timeout en intento {intento}")
        
        except aiohttp.ClientError as e:
            print(f"  ❌ Error de red: {e}")
        
        # Si no es el último intento, esperar con backoff exponencial
        if intento < max_intentos:
            # Backoff exponencial con jitter
            espera = backoff_base * (2 ** (intento - 1))
            jitter = random.uniform(0, espera * 0.1)  # ±10% de variación
            tiempo_total = espera + jitter
            
            print(f"  ⏳ Esperando {tiempo_total:.2f}s antes de reintentar...")
            await asyncio.sleep(tiempo_total)
    
    print(f"  💔 Fallaron todos los intentos para {url}")
    return None

async def main():
    urls = [
        "https://httpbin.org/status/200",  # Siempre exitoso
        "https://httpbin.org/status/500",  # Siempre falla (servidor)
        "https://httpbin.org/status/404",  # Error cliente (no reintentable)
        "https://httpbin.org/delay/10",    # Timeout
    ]
    
    async with aiohttp.ClientSession() as session:
        tareas = [
            fetch_con_retry(session, url, max_intentos=3, backoff_base=1)
            for url in urls
        ]
        
        resultados = await asyncio.gather(*tareas)
    
    exitosos = sum(1 for r in resultados if r is not None)
    print(f"\n📊 Resultados: {exitosos}/{len(urls)} exitosos")

if __name__ == "__main__":
    asyncio.run(main())