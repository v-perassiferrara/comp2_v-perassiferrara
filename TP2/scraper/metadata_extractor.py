"""
Extracción de metadatos de páginas web
"""


class MetadataExtractor:
    """Extractor de metadatos HTML"""
    
    @staticmethod
    def extract_meta_tags(soup):
        """Extrae meta tags relevantes (description, keywords, Open Graph)"""
        meta_tags = {}
        
        # Description
        desc = soup.find('meta', attrs={'name': 'description'})
        if desc and desc.get('content'):
            meta_tags['description'] = desc['content']
        
        # Keywords
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        if keywords and keywords.get('content'):
            meta_tags['keywords'] = keywords['content']
        
        # Open Graph tags
        og_tags = soup.find_all('meta', attrs={'property': lambda x: x and x.startswith('og:')})
        for tag in og_tags:
            if tag.get('content'):
                meta_tags[tag['property']] = tag['content']
        
        # Twitter cards
        twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})
        for tag in twitter_tags:
            if tag.get('content'):
                meta_tags[tag['name']] = tag['content']
        
        return meta_tags
    
    @staticmethod
    def extract_all_metadata(soup):
        """Extrae todos los metadatos disponibles"""
        return MetadataExtractor.extract_meta_tags(soup)
