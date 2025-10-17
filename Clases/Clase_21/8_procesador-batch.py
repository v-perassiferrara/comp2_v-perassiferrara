import aiofiles
import asyncio
import random

'''
Ejercicio 8: Procesador de archivos batch

Objetivo: Leer múltiples archivos de texto concurrentemente y contar palabras totales.

Requisitos:

    Crear 5 archivos de texto con contenido dummy
    Leer todos los archivos concurrentemente usando aiofiles
    Contar palabras en cada archivo
    Calcular estadísticas: total de palabras, promedio por archivo, archivo más largo
    Simular procesamiento lento con await asyncio.sleep(random.uniform(0.1, 0.5))

Pistas:

    aiofiles.open(archivo, 'r') para lectura asíncrona
    .split() para contar palabras
    asyncio.gather() con return_exceptions=True para manejar errores

'''


async def leer_archivo(archivo):
    async with aiofiles.open(archivo, 'r') as f:
        contenido = await f.read()
        palabras = contenido.split()
        await asyncio.sleep(random.uniform(0.1, 0.5))
        return len(palabras), archivo

async def procesar_archivos(archivos):
    tareas = [leer_archivo(archivo) for archivo in archivos]
    resultados = await asyncio.gather(*tareas, return_exceptions=True)
    total_palabras = 0
    archivo_mas_largo = ""
    max_num_palabras = 0
    for resultado in resultados:
        if isinstance(resultado, Exception):
            print(f"Error leyendo archivo: {resultado}")
        else:
            num_palabras, archivo = resultado
            total_palabras += num_palabras
            if num_palabras > max_num_palabras:
                max_num_palabras = num_palabras
                archivo_mas_largo = archivo.split("/")[-1]
    
    promedio_palabras = total_palabras / len(archivos)
    print(f"Promedio de palabras por archivo: {promedio_palabras:.2f}")
    print(f"Archivo más largo: {archivo_mas_largo} con {max_num_palabras} palabras")

async def main():
    archivos = [
        "textos/a.txt",
        "textos/e.txt",
        "textos/i.txt",
        "textos/o.txt",
        "textos/u.txt",
    ]
    
    await procesar_archivos(archivos)


if __name__ == "__main__":
    asyncio.run(main())
