import threading
import requests # Necesitarás instalarlo: pip install requests
import time

# Lista de URLs para crawlear (puedes añadir más o diferentes)
URLS_TO_CRAWL = [
    "[http://python.org](http://python.org)",
    "[http://example.com](http://example.com)",
    "[https://www.djangoproject.com/](https://www.djangoproject.com/)",
    "[https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)",
    "[http://invalid.url.that.will.fail](http://invalid.url.that.will.fail)", # URL para probar manejo de errores
    "[https://docs.python.org/3/library/threading.html](https://docs.python.org/3/library/threading.html)"
]

# Diccionario compartido para almacenar resultados (URL: tamaño_html)
# Protegido por un lock
results = {}
results_lock = threading.Lock()

# Contador para saber cuántos hilos han terminado
# Protegido por un lock
active_threads_count = 0
active_threads_lock = threading.Lock()


def crawl_url(url, thread_id):
    global active_threads_count
    print(f"Hilo {thread_id}: Iniciando crawl para {url}")
    html_content = None
    content_size = -1 # Indica error o no encontrado

    try:
        response = requests.get(url, timeout=5) # Timeout de 5 segundos
        response.raise_for_status() # Lanza excepción para errores HTTP (4xx o 5xx)
        html_content = response.text
        content_size = len(html_content)
        print(f"Hilo {thread_id}: {url} descargado exitosamente ({content_size} bytes).")
    except requests.exceptions.RequestException as e:
        print(f"Hilo {thread_id}: Error al crawlear {url}: {e}")
    
    # Sección crítica: Actualizar el diccionario de resultados
    with results_lock:
        results[url] = content_size
    
    # Sección crítica: Decrementar contador de hilos activos
    # Aunque en este caso el join() del principal lo maneja,
    # es un patrón útil si no se usa join() en todos.
    with active_threads_lock:
        active_threads_count -=1
        print(f"Hilo {thread_id}: Terminado. Hilos activos restantes: {active_threads_count}")


if __name__ == "__main__":
    start_time = time.time()
    threads = []
    
    active_threads_count = len(URLS_TO_CRAWL) # Inicializar contador

    print(f"Iniciando crawling de {len(URLS_TO_CRAWL)} URLs con {len(URLS_TO_CRAWL)} hilos...")

    for i, url in enumerate(URLS_TO_CRAWL):
        thread = threading.Thread(target=crawl_url, args=(url, i), name=f"Crawler-{i}")
        threads.append(thread)
        thread.start()

    # Esperar a que todos los hilos terminen
    print("\nHilo Principal: Esperando a que todos los hilos del crawler terminen...")
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    
    print("\n--- Resultados del Crawling ---")
    for url, size in results.items():
        if size != -1:
            print(f"URL: {url} -> Tamaño: {size} bytes")
        else:
            print(f"URL: {url} -> Falló la descarga")
            
    print(f"\nCrawling completado en {end_time - start_time:.2f} segundos.")