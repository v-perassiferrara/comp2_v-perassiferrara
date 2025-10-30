import unittest
import os
import sys
import base64

# Add the project root to the sys.path to allow imports from processor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from processor.screenshot import capture_screenshot
from processor.performance import analyze_performance
from processor.image_processor import process_images

# A simple, reliable URL for testing
TEST_URL = "http://example.com"

class TestProcessor(unittest.TestCase):

    def test_capture_screenshot(self):
        """Smoke test for the screenshot capture function."""
        screenshot_b64 = capture_screenshot(TEST_URL)
        self.assertIsNotNone(screenshot_b64)
        self.assertIsInstance(screenshot_b64, str)
        # Check if it's valid base64
        try:
            base64.b64decode(screenshot_b64)
        except Exception as e:
            self.fail(f"Screenshot is not valid base64: {e}")

    def test_analyze_performance(self):
        """Smoke test for the performance analysis function."""
        performance_data = analyze_performance(TEST_URL)
        self.assertIsNotNone(performance_data)
        self.assertIsInstance(performance_data, dict)
        self.assertIn('load_time_ms', performance_data)
        self.assertIn('total_size_kb', performance_data)
        self.assertIn('num_requests', performance_data)
        self.assertGreater(performance_data['load_time_ms'], 0)
        self.assertGreaterEqual(performance_data['num_requests'], 1)

    def test_process_images(self):
        """Smoke test for the image processing function."""
        # example.com has no images, so we expect an empty list.
        # This tests that the function handles pages with no images gracefully.
        thumbnails = process_images(TEST_URL)
        self.assertIsNotNone(thumbnails)
        self.assertIsInstance(thumbnails, list)
        self.assertEqual(len(thumbnails), 0)

if __name__ == '__main__':
    # Note: These tests perform network requests and can be slow.
    unittest.main()
