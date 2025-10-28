import time
from playwright.sync_api import sync_playwright

def performance(url: str) -> bytes:
    """
    Mide el tiempo de carga de una pagina web para una URL dada.

    Argumentos:
        url: La URL a medir.

    Retorna:
        Un string con el tiempo de carga, en ASCII.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        start_time = time.time()
        try:
            page.goto(url, timeout=60000) # Timeout de 60 segundos
            end_time = time.time()
            load_time = end_time - start_time
            response = f"Tiempo de carga para {url}: {load_time:.2f} segundos"
        except Exception as e:
            print(f"Error midiendo rendimiento para {url}: {e}")
            response = f"Error al medir rendimiento para {url}."
        finally:
            browser.close()

    return response.encode('ascii')

