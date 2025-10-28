import base64
from playwright.sync_api import sync_playwright

def screenshot(url: str) -> bytes:
    """
    Navega a una URL y toma una captura de pantalla.

    Argumentos:
        url: La URL a visitar.

    Retorna:
        La imagen de la captura de pantalla en bytes codificados en base64.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=60000)  # Timeout de 60 segundos
            screenshot_bytes = page.screenshot()
        except Exception as e:
            print(f"Error al sacar screenshot de {url}: {e}")
            # Retornar un string de bytes vacio o una imagen de marcador de posicion en caso de error
            return b""
        finally:
            browser.close()

    if screenshot_bytes:
        return base64.b64encode(screenshot_bytes)
    return b""

