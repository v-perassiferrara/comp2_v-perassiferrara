"""
Generación de screenshots de páginas web
"""
import base64
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def capture_screenshot(url, full_page=False, timeout=30000):
    """
    Captura un screenshot de la página web
    
    Args:
        url: URL de la página
        full_page: Si True, captura la página completa
        timeout: Timeout en milisegundos
    
    Returns:
        Screenshot en base64 o None si hay error
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navegar a la página
            page.goto(url, timeout=timeout, wait_until='networkidle')
            
            # Capturar screenshot
            screenshot_bytes = page.screenshot(full_page=full_page)
            
            browser.close()
            
            # Convertir a base64
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            return screenshot_b64
            
    except PlaywrightTimeoutError:
        print(f"Timeout capturando screenshot de: {url}")
        return None
    except Exception as e:
        print(f"Error capturando screenshot: {e}")
        return None
