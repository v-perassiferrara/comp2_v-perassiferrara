
'''
Ejercicio 4: Monitor de recursos del sistema
Objetivo: Monitorear CPU, memoria y disco cada 5 segundos usando threads.

Requisitos:

Crear 3 funciones: monitorear_cpu(), monitorear_memoria(), monitorear_disco()
Cada función lee métricas cada 5s y las guarda en una lista compartida
Usar ThreadPoolExecutor con 3 workers permanentes
Función principal que cada 30s calcula promedios y muestra reporte
Graceful shutdown con Ctrl+C
'''


import psutil
import time
import threading
from concurrent.futures import ThreadPoolExecutor

detenerse = threading.Event()

def monitorear_cpu(resultados, intervalo=2):
    while not detenerse.is_set():
        cpu = psutil.cpu_percent(interval=1)
        if cpu is not None:
            resultados['cpu'].append(cpu)
        time.sleep(intervalo)

def monitorear_memoria(resultados, intervalo=2):
    while not detenerse.is_set():
        mem = psutil.virtual_memory().percent
        resultados['memoria'].append(mem)
        time.sleep(intervalo)

def monitorear_disco(resultados, intervalo=2):
    while not detenerse.is_set():
        disco = psutil.disk_usage('/').percent
        resultados['disco'].append(disco)
        time.sleep(intervalo)

def promediar(lista):
    return sum(lista) / len(lista) if lista else 0

if __name__ == "__main__":
    resultados = {
        'cpu': [],
        'memoria': [],
        'disco': []
    }

    executor = ThreadPoolExecutor(max_workers=3)
    
    try:
        print("Iniciando monitoreo de recursos... (Presiona Ctrl+C para detener)")
        
        # Iniciar los monitores
        executor.submit(monitorear_cpu, resultados)
        executor.submit(monitorear_memoria, resultados)
        executor.submit(monitorear_disco, resultados)

        while True:
            time.sleep(8)
            
            print("\n--- Reporte de Recursos (promedio últimos 8s) ---")
            
            # Calcular promedios
            avg_cpu = promediar(resultados['cpu'])
            avg_memoria = promediar(resultados['memoria'])
            avg_disco = promediar(resultados['disco'])

            print(f"CPU: {avg_cpu:.2f}%")
            print(f"Memoria: {avg_memoria:.2f}%")
            print(f"Disco: {avg_disco:.2f}%")
            
            # Limpiar listas para el próximo intervalo
            for key in resultados.keys():
                resultados[key].clear()

    except KeyboardInterrupt:
        print("\nDeteniendo el monitoreo...")
        detenerse.set()
        executor.shutdown(wait=True)
        print("Monitoreo detenido.")
