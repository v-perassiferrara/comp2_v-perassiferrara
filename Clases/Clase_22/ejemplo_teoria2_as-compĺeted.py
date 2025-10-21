# Permite procesar a medida que terminan

from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

def tarea(id):
    duracion = random.uniform(1, 3)
    time.sleep(duracion)
    return f"Tarea {id} tardó {duracion:.2f}s"

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(tarea, i) for i in range(5)] # Crear 5 futures
    
    # Procesar según terminan (no en orden)
    for future in as_completed(futures): # Se van encolando los futures que van terminando
        print(future.result())