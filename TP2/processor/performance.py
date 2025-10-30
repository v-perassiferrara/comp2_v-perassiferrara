"""
Análisis de rendimiento de páginas web
"""
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def analyze_performance(url, timeout=30000):
    """
    Analiza el rendimiento de carga de la página
    
    Args:
        url: URL de la página
        timeout: Timeout en milisegundos
    
    Returns:
        Diccionario con métricas de rendimiento
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            start_time = time.time()
            
            # Capturar todas las requests
            requests = []
            total_size = 0
            
            def handle_response(response):
                nonlocal total_size
                try:
                    headers = response.headers
                    content_length = headers.get('content-length', '0')
                    if content_length.isdigit():
                        total_size += int(content_length)
                    requests.append(response.url)
                except Exception:
                    pass  # Ignorar errores en responses individuales
            
            page.on('response', handle_response)
            
            # Navegar a la página
            page.goto(url, timeout=timeout, wait_until='networkidle')
            
            load_time = (time.time() - start_time) * 1000  # en ms
            
            browser.close()
            
            return {
                'load_time_ms': round(load_time, 2),
                'total_size_kb': round(total_size / 1024, 2),
                'num_requests': len(requests)
            }
            
    except PlaywrightTimeoutError:
        print(f"Timeout analizando rendimiento de: {url}")
        return {
            'load_time_ms': 0,
            'total_size_kb': 0,
            'num_requests': 0,
            'error': 'Timeout'
        }
    except Exception as e:
        print(f"Error analizando rendimiento: {e}")
        return {
            'load_time_ms': 0,
            'total_size_kb': 0,
            'num_requests': 0,
            'error': str(e)
        }
