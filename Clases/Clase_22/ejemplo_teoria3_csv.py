from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import numpy as np
import time

def procesar_chunk(chunk_data):
    """Procesa un chunk de datos (CPU-bound)"""
    chunk_id, df_chunk = chunk_data
    
    # Operaciones pesadas
    df_chunk['cuadrado'] = df_chunk['valor'] ** 2
    df_chunk['raiz'] = np.sqrt(df_chunk['valor'])
    df_chunk['log'] = np.log(df_chunk['valor'] + 1)
    
    # Agregaciones
    estadisticas = {
        'chunk_id': chunk_id,
        'filas': len(df_chunk),
        'suma': df_chunk['valor'].sum(),
        'promedio': df_chunk['valor'].mean(),
        'std': df_chunk['valor'].std(),
    }
    
    return estadisticas

def crear_csv_prueba(nombre, num_filas=1_000_000):
    """Crea un CSV de prueba"""
    df = pd.DataFrame({
        'id': range(num_filas),
        'valor': np.random.randint(1, 1000, num_filas),
        'categoria': np.random.choice(['A', 'B', 'C'], num_filas)
    })
    df.to_csv(nombre, index=False)
    print(f"Creado {nombre} con {num_filas:,} filas")

def procesar_csv_paralelo(archivo, chunk_size=100_000, max_workers=4):
    """Lee CSV en chunks y procesa en paralelo"""
    inicio = time.time()
    
    # Leer chunks
    chunks = []
    for i, chunk in enumerate(pd.read_csv(archivo, chunksize=chunk_size)):
        chunks.append((i, chunk))
    
    print(f"CSV dividido en {len(chunks)} chunks")
    
    # Procesar en paralelo
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        resultados = list(executor.map(procesar_chunk, chunks))
    
    # Consolidar resultados
    total_filas = sum(r['filas'] for r in resultados)
    suma_total = sum(r['suma'] for r in resultados)
    promedio_global = suma_total / total_filas
    
    duracion = time.time() - inicio
    
    print(f"\n✓ Procesadas {total_filas:,} filas en {duracion:.2f}s")
    print(f"  Suma total: {suma_total:,.0f}")
    print(f"  Promedio: {promedio_global:.2f}")
    
    return resultados

# Uso
if __name__ == "__main__":
    archivo = "datos_grandes.csv"
    
    # Crear archivo de prueba si no existe
    from pathlib import Path
    if not Path(archivo).exists():
        crear_csv_prueba(archivo, num_filas=1_000_000)
    
    # Procesar
    resultados = procesar_csv_paralelo(
        archivo, 
        chunk_size=100_000,
        max_workers=4
    )