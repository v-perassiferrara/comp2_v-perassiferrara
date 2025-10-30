"""
Módulo de procesamiento de páginas web
"""
from .screenshot import capture_screenshot
from .performance import analyze_performance
from .image_processor import process_images

__all__ = ['capture_screenshot', 'analyze_performance', 'process_images']
