import unittest
import os
import sys
import base64

# Agrega el directorio raíz del proyecto a sys.path para permitir importaciones desde processor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from processor.screenshot import capture_screenshot
from processor.performance import analyze_performance
from processor.image_processor import process_images

# Una URL simple y confiable para las pruebas
TEST_URL = "http://example.com"

class TestProcessor(unittest.TestCase):

    def test_capture_screenshot(self):
        """Prueba de humo para la función de captura de pantalla."""
        screenshot_b64 = capture_screenshot(TEST_URL)
        self.assertIsNotNone(screenshot_b64)
        self.assertIsInstance(screenshot_b64, str)
        # Verificar si es base64 válido
        try:
            base64.b64decode(screenshot_b64)
        except Exception as e:
            self.fail(f"La captura de pantalla no es un base64 válido: {e}")

    def test_analyze_performance(self):
        """Prueba de humo para la función de análisis de rendimiento."""
        performance_data = analyze_performance(TEST_URL)
        self.assertIsNotNone(performance_data)
        self.assertIsInstance(performance_data, dict)
        self.assertIn('load_time_ms', performance_data)
        self.assertIn('total_size_kb', performance_data)
        self.assertIn('num_requests', performance_data)
        self.assertGreater(performance_data['load_time_ms'], 0)
        self.assertGreaterEqual(performance_data['num_requests'], 1)

    def test_process_images(self):
        """Prueba de humo para la función de procesamiento de imágenes."""
        # example.com no tiene imágenes, por lo que esperamos una lista vacía.
        # Esto prueba que la función maneja páginas sin imágenes correctamente.
        thumbnails = process_images(TEST_URL)
        self.assertIsNotNone(thumbnails)
        self.assertIsInstance(thumbnails, list)
        self.assertEqual(len(thumbnails), 0)

if __name__ == '__main__':
    # Nota: Estas pruebas realizan solicitudes de red y pueden ser lentas.
    unittest.main()
