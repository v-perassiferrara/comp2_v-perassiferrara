"""
Cliente HTTP asíncrono para scraping
"""
import asyncio
import aiohttp


class AsyncHTTPClient:
    """Cliente HTTP asíncrono"""
    
    def __init__(self, timeout=30):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
    
    async def fetch(self, url):
        """Realiza una petición HTTP asíncrona"""
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}")
                return await response.text()
    
    async def fetch_multiple(self, urls):
        """Realiza múltiples peticiones HTTP en paralelo"""
        tasks = [self.fetch(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
