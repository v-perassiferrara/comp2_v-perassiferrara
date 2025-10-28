import base64
import requests
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

def image_processor(url: str) -> bytes:
    """
    - Obtiene URLs de imagenes de una pagina web.
    - Descarga las primeras 5 imagenes.
    - Redimensiona a miniaturas de 100x100.
    - Retorna las miniaturas como un unico objeto de bytes, con cada imagen
      codificada en base64 y separada por un salto de linea.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        thumbnails = []

        try:
            page.goto(url, timeout=60000) # Timeout de 60 segundos

            image_urls = page.eval_on_selector_all("img", "elements => elements.map(el => el.src)") # Obtener URLs de cada imagen

            # Convertir URLs a absolutas
            absolute_image_urls = [urljoin(url, img_url) for img_url in image_urls]

            for img_url in absolute_image_urls[:5]: # Procesar las primeras 5 imagenes
                try:
                    # Filtrar URLs no HTTP y/o sin una extension de imagen comun (que Pillow soporte por defecto)
                    supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
                    if not img_url.startswith('http') or not img_url.lower().endswith(supported_extensions):
                        print(f"Omitiendo imagen no soportada: {img_url[:80]}...")
                        continue

                    response = requests.get(img_url, timeout=10)
                    response.raise_for_status() # Lanzar una excepcion para codigos de estado incorrectos

                    img = Image.open(BytesIO(response.content))
                    img.thumbnail((100, 100))

                    buffered = BytesIO()
                    img.save(buffered, format="PNG") # Guardar como PNG

                    encoded_img = base64.b64encode(buffered.getvalue())
                    thumbnails.append(encoded_img)

                except requests.exceptions.RequestException as e:
                    print(f"No se pudo descargar la imagen {img_url}: {e}")
                except Exception as e:
                    print(f"No se pudo procesar la imagen {img_url}: {e}")

        except Exception as e:
            print(f"Error al procesar la página {url}: {e}")
            return f"Error al procesar la página {url}.".encode('ascii')
        finally:
            browser.close()

    # Unir las miniaturas en base64 como una sola cadena, separadas por líneas
    return b"\n".join(thumbnails)
