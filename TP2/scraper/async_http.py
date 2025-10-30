"""
Cliente HTTP asíncrono para scraping
"""
import asyncio
import aiohttp


class AsyncHTTPClient:
    """Cliente HTTP asíncrono con gestión eficiente de sesiones"""
    
    def __init__(self, timeout=30):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = None
    
    async def __aenter__(self):
        """Context manager entry - crea la sesión"""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cierra la sesión"""
        if self.session:
            await self.session.close()
        return False
    
    async def fetch(self, url):
        """Realiza una petición HTTP asíncrona"""
        if not self.session:
            raise RuntimeError("AsyncHTTPClient debe usarse como context manager")
        
        async with self.session.get(url) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}")
            return await response.text()
    
    async def fetch_multiple(self, urls):
        """Realiza múltiples peticiones HTTP en paralelo"""
        if not self.session:
            raise RuntimeError("AsyncHTTPClient debe usarse como context manager")
        
        tasks = [self.fetch(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
