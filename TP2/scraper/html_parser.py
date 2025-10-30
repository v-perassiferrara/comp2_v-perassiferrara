"""
Funciones de parsing HTML
"""
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class HTMLParser:
    """Parser de contenido HTML"""
    
    @staticmethod
    def parse_html(html_content):
        """Parsea el contenido HTML"""
        return BeautifulSoup(html_content, 'lxml')
    
    @staticmethod
    def extract_links(soup, base_url, limit=50):
        """Extrae todos los enlaces de la página"""
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            absolute_url = urljoin(base_url, href)
            if absolute_url not in links:
                links.append(absolute_url)
        return links[:limit]
    
    @staticmethod
    def extract_structure(soup):
        """Extrae la estructura de headers H1-H6"""
        structure = {}
        for i in range(1, 7):
            headers = soup.find_all(f'h{i}')
            if headers:
                structure[f'h{i}'] = len(headers)
        return structure
    
    @staticmethod
    def extract_title(soup):
        """Extrae el título de la página"""
        return soup.title.string if soup.title else 'Sin título'
    
    @staticmethod
    def count_images(soup):
        """Cuenta las imágenes en la página"""
        return len(soup.find_all('img'))
