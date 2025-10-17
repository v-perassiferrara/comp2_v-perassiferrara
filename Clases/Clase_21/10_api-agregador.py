import aiohttp
import asyncio
from datetime import datetime

'''
Ejercicio 10: API agregador

Objetivo: Crear un programa que consulte múltiples APIs de clima y devuelva el promedio.

Requisitos:

    Consultar al menos 3 APIs de clima diferentes (o usa APIs mock)
    Extraer temperatura de cada respuesta (formato JSON diferente)
    Calcular temperatura promedio
    Si una API falla, usar solo las que funcionaron
    Timeout de 3 segundos por API

APIs sugeridas (o usa httpbin para simular):

    OpenWeatherMap (requiere API key gratuita)
    WeatherAPI (requiere API key gratuita)
    O simula con https://httpbin.org/json modificando la respuesta

Pistas:

    Usa asyncio.gather(*tareas, return_exceptions=True)
    Filtra resultados exitosos vs excepciones
    Maneja JSONs con estructuras diferentes

'''


TIMEOUT_SEGUNDOS = 3

ESTRATEGIAS_EXTRACCION = { # para manejar la estructura de los datos de cada API
    "clima1": ["args", "temperature"],
    "clima2": ["args", "temp_celsius"],
    "clima3": ["args", "value"],
}

def extraer_temperatura(resultado_api):
    """
    Usa el diccionario de estrategias para extraer la temperatura de forma genérica.
    """
    api_nombre = resultado_api['api']
    
    # Busca la ruta de claves para esta API en el diccionario
    ruta = ESTRATEGIAS_EXTRACCION.get(api_nombre)
    
    if not ruta: # si no hay estrategia, no extraemos nada
        print(f"🔍 No hay estrategia de extracción para '{api_nombre}'")
        return None

    try:
        # Sigue la ruta de claves para navegar el JSON y obtener el valor
        valor = resultado_api['datos']
        for clave in ruta:
            valor = valor[clave]
        
        return float(valor)

    except (KeyError, ValueError, TypeError):
        print(f"🔍 Falló la extracción para '{api_nombre}' con la ruta {ruta}")
        return None






async def consultar_api(session, nombre, url, TIMEOUT_SEGUNDOS):
    """Consulta una API con timeout"""
    try:
        inicio = datetime.now()
        
        # timeout_segundos aplica a toda la operación
        timeout = aiohttp.ClientTimeout(total=TIMEOUT_SEGUNDOS)
        
        async with session.get(url, timeout=timeout) as response:
            datos = await response.json()
            
            duracion = (datetime.now() - inicio).total_seconds()
            print(f"✅ {nombre}: {response.status} ({duracion:.2f}s)\n")
            return {"api": nombre, "datos": datos, "duracion": duracion}
            
    except asyncio.TimeoutError:
        print(f"⏱️  {nombre}: Timeout después de {TIMEOUT_SEGUNDOS}s")
        return {"api": nombre, "error": "timeout"}
        
    except Exception as e:
        print(f"❌ {nombre}: Error - {e}")
        return {"api": nombre, "error": str(e)}

async def main():
    
    # hice uso de httpbun en lugar de bin porque este no me funcionaba
    
    apis = [
        ("clima1",'https://httpbun.com/get?temperature=24.8'),
        ("clima2",'https://httpbun.com/get?temp_celsius=23.4'),
        ("clima3",'https://httpbun.com/get?value=27'),
    ]
    
    async with aiohttp.ClientSession() as session:
        tareas = [
            consultar_api(session, nombre, url, TIMEOUT_SEGUNDOS)
            for nombre, url in apis
        ]
        
        resultados = await asyncio.gather(*tareas)
    
    print("\n📊 Resumen:")
    for resultado in resultados:
        print(f"  {resultado['api']}: {resultado.get('error', 'OK')}")



    temperaturas_validas = []
    
    for resultado in resultados:
        # Solo procesamos los resultados que no tuvieron errores de conexión
        if "error" not in resultado:
            temp = extraer_temperatura(resultado)
            if temp is not None:
                temperaturas_validas.append(temp)
    
    
    # Calculamos el promedio solo si tenemos al menos una temperatura válida
    if temperaturas_validas:
        promedio = sum(temperaturas_validas) / len(temperaturas_validas)
        print(f"\nTemperaturas obtenidas: {temperaturas_validas}")
        print(f"   Promedio final: {promedio:.2f}°C")
    else:
        print("\n❌ No se pudo obtener ninguna temperatura para calcular el promedio.")

if __name__ == "__main__":
    asyncio.run(main())