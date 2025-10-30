"""
Procesamiento de imágenes de páginas web
"""
import base64
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import requests
from urllib.parse import urljoin


def process_images(url, max_images=3, thumbnail_size=(150, 150), timeout=30000):
    """
    Descarga y procesa imágenes principales de la página
    
    Args:
        url: URL de la página
        max_images: Número máximo de imágenes a procesar
        thumbnail_size: Tamaño de los thumbnails (ancho, alto)
        timeout: Timeout en milisegundos
    
    Returns:
        Lista de thumbnails en base64
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=timeout, wait_until='networkidle')
            
            # Obtener URLs de imágenes
            img_urls = page.evaluate(f'''() => {{
                const imgs = Array.from(document.querySelectorAll('img'));
                return imgs.slice(0, {max_images}).map(img => img.src);
            }}''')
            
            browser.close()
            
            thumbnails = []
            for img_url in img_urls:
                if not img_url:
                    continue
                
                try:
                    absolute_img_url = urljoin(url, img_url)

                    # Validar que sea HTTP/HTTPS
                    if not absolute_img_url.startswith(('http://', 'https://')):
                        continue
                    
                    # Filtrar extensiones soportadas
                    supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
                    if not absolute_img_url.lower().endswith(supported_extensions):
                        # Intentar de todos modos si no tiene extensión obvia
                        if '.' in absolute_img_url.split('/')[-1]:
                            continue

                    # Descargar imagen
                    response = requests.get(absolute_img_url, timeout=5, stream=True)
                    if response.status_code == 200:
                        # Intentar abrir la imagen
                        try:
                            img = Image.open(BytesIO(response.content))
                            
                            # Crear thumbnail
                            img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
                            
                            # Convertir a base64
                            buffered = BytesIO()
                            
                            # Convertir a RGB si es necesario (para PNG con transparencia)
                            if img.mode in ('RGBA', 'LA', 'P'):
                                background = Image.new('RGB', img.size, (255, 255, 255))
                                if img.mode == 'P':
                                    img = img.convert('RGBA')
                                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                                img = background
                            
                            img.save(buffered, format="JPEG", quality=85)
                            thumb_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                            thumbnails.append(thumb_b64)
                        except (IOError, OSError) as e:
                            print(f"Error procesando imagen {img_url}: No es una imagen válida - {e}")
                            continue
                    
                except requests.RequestException as e:
                    print(f"Error descargando imagen {img_url}: {e}")
                    continue
                except Exception as e:
                    print(f"Error inesperado procesando imagen {img_url}: {e}")
                    continue
            
            return thumbnails
            
    except PlaywrightTimeoutError:
        print(f"Timeout al cargar la página para procesar imágenes: {url}")
        return []
    except Exception as e:
        print(f"Error procesando imágenes: {e}")
        return []
