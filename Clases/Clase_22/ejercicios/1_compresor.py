'''
Ejercicio 1: Compresor de archivos paralelo
Objetivo: Comprimir múltiples archivos en paralelo usando diferentes algoritmos.

Requisitos:

Crear 10 archivos de texto con contenido aleatorio
Comprimir cada uno con gzip usando ProcessPoolExecutor
Comparar tiempo secuencial vs paralelo
Calcular ratio de compresión promedio
Mostrar progreso: "Comprimido 3/10 archivos..."
'''


import gzip
import shutil
from pathlib import Path
import random
import string
import time
from concurrent.futures import ProcessPoolExecutor, as_completed




def crear_archivos_de_prueba(directorio, num_archivos=10):
    dir_path = Path(directorio)
    dir_path.mkdir(exist_ok=True)
    
    archivos_creados = []
    contenido = ''.join(random.choices(string.ascii_letters, k=1024 * 1024))    
                                                    # k es el tamaño del archivo = 1MB
    
    for i in range(num_archivos):
        ruta_archivo = dir_path / f"archivo_{i+1}.txt"
        with open(ruta_archivo, 'w') as f:
            f.write(contenido)
        archivos_creados.append(ruta_archivo)
    return archivos_creados






def comprimir_archivo(ruta_entrada):
    ruta_salida = ruta_entrada.with_suffix('.gz')
    with open(ruta_entrada, 'rb') as f_in:
        with gzip.open(ruta_salida, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    return {
        'archivo': ruta_entrada.name,
        'tamaño_original': ruta_entrada.stat().st_size,
        'tamaño_comprimido': ruta_salida.stat().st_size
    }




def main():
    directorio_prueba = "temp_archivos_a_comprimir"
    num_archivos = 5


    # Crear archivos de prueba
    archivos = crear_archivos_de_prueba(directorio_prueba, num_archivos)
    print("Archivos creados.")



    # Compresión secuencial
    print("--- Compresión Secuencial ---")
    inicio_secuencial = time.time()
    stats_secuencial = []
    for i, archivo in enumerate(archivos):
        stats = comprimir_archivo(archivo)
        stats_secuencial.append(stats)
        print(f"Comprimido {i+1}/{num_archivos} archivos...")
    fin_secuencial = time.time()
    tiempo_secuencial = fin_secuencial - inicio_secuencial
    print(f"Tiempo total (secuencial): {tiempo_secuencial:.4f} segundos")



    # Compresión paralela
    print("--- Compresión Paralela (ProcessPoolExecutor) ---")
    inicio_paralelo = time.time()
    stats_paralelo = []
    with ProcessPoolExecutor() as executor:
        futuros = [executor.submit(comprimir_archivo, archivo) for archivo in archivos]
        
        for i, futuro in enumerate(as_completed(futuros)):
            stats = futuro.result()
            stats_paralelo.append(stats)
            print(f"Comprimido {i+1}/{num_archivos} archivos...")
            
    fin_paralelo = time.time()
    tiempo_paralelo = fin_paralelo - inicio_paralelo
    print(f"Tiempo total (paralelo): {tiempo_paralelo:.4f} segundos")



    # Comparación y ratio
    print("--- Resultados ---")
    print(f"Mejora de tiempo con paralelismo: {tiempo_secuencial / tiempo_paralelo:.2f}x")

    total_original = sum(s['tamaño_original'] for s in stats_paralelo)
    total_comprimido = sum(s['tamaño_comprimido'] for s in stats_paralelo)
    
    if total_comprimido > 0:
        ratio_promedio = total_original / total_comprimido
        print(f"Tamaño total original: {total_original / (1024*1024):.2f} MB")
        print(f"Tamaño total comprimido: {total_comprimido / (1024*1024):.2f} MB")
        print(f"Ratio de compresión promedio: {ratio_promedio:.2f}:1")
    else:
        print("No se pudo calcular el ratio de compresión.")



    # Limpieza
    shutil.rmtree(directorio_prueba)
    print("Limpieza completada.")




if __name__ == "__main__":
    main()
