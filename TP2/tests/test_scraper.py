import unittest
import os
import sys

# Agrega el directorio raíz del proyecto a sys.path para permitir importaciones desde scraper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper.html_parser import HTMLParser

class TestHTMLParser(unittest.TestCase):

    def test_extract_title(self):
        """Prueba que el título se extraiga correctamente del HTML."""
        html_content = "<html><head><title>Página de Prueba</title></head><body></body></html>"
        soup = HTMLParser.parse_html(html_content)
        title = HTMLParser.extract_title(soup)
        self.assertEqual(title, "Página de Prueba")

    def test_extract_title_no_title(self):
        """Prueba el comportamiento cuando no hay etiqueta de título."""
        html_content = "<html><head></head><body></body></html>"
        soup = HTMLParser.parse_html(html_content)
        title = HTMLParser.extract_title(soup)
        self.assertEqual(title, "Sin título")

    def test_count_images(self):
        """Prueba que el número de imágenes se cuente correctamente."""
        html_content = """
        <html><body>
            <img src="image1.jpg">
            <img src="image2.png">
            <img src="image3.gif">
        </body></html>
        """
        soup = HTMLParser.parse_html(html_content)
        count = HTMLParser.count_images(soup)
        self.assertEqual(count, 3)

    def test_count_images_no_images(self):
        """Prueba el comportamiento cuando no hay imágenes."""
        html_content = "<html><body><p>No hay imágenes.</p></body></html>"
        soup = HTMLParser.parse_html(html_content)
        count = HTMLParser.count_images(soup)
        self.assertEqual(count, 0)

    def test_extract_links(self):
        """Prueba que los enlaces se extraigan y se conviertan a rutas absolutas."""
        html_content = """
        <html><body>
            <a href="/page1.html">Página 1</a>
            <a href="https://example.com/page2.html">Página 2</a>
            <a href="page3.html">Página 3</a>
        </body></html>
        """
        base_url = "http://test.com"
        soup = HTMLParser.parse_html(html_content)
        links = HTMLParser.extract_links(soup, base_url)
        
        expected_links = [
            "http://test.com/page1.html",
            "https://example.com/page2.html",
            "http://test.com/page3.html"
        ]
        self.assertEqual(len(links), 3)
        self.assertCountEqual(links, expected_links) # Usa assertCountEqual para una comparación insensible al orden

if __name__ == '__main__':
    unittest.main()
