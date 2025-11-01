"""
Cliente HTTP asíncrono para scraping
"""
import asyncio
import aiohttp
from aiohttp import ClientTimeout, ClientError


class AsyncHTTPClient:
    """Cliente HTTP asíncrono con gestión eficiente de sesiones"""
    
    def __init__(self, timeout=30, max_redirects=10):
        """
        Inicializa el cliente HTTP asíncrono
        
        Args:
            timeout: Timeout total en segundos
            max_redirects: Número máximo de redirecciones
        """
        self.timeout = ClientTimeout(
            total=timeout,
            connect=10,  # Timeout de conexión
            sock_read=timeout  # Timeout de lectura
        )
        self.max_redirects = max_redirects
        self.session = None
    
    async def __aenter__(self):
        """Context manager entry - crea la sesión"""
        connector = aiohttp.TCPConnector(
            limit=100,  # Límite de conexiones totales
            limit_per_host=10,  # Límite por host
            ttl_dns_cache=300  # Cache DNS de 5 minutos
        )
        
        self.session = aiohttp.ClientSession(
            timeout=self.timeout,
            connector=connector,
            raise_for_status=False  # No lanzar excepción automáticamente
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cierra la sesión"""
        if self.session:
            await self.session.close()
            # Esperar un poco para que las conexiones se cierren correctamente
            await asyncio.sleep(0.1)
        return False
    
    async def fetch(self, url, headers=None):
        """
        Realiza una petición HTTP asíncrona
        
        Args:
            url: URL a solicitar
            headers: Headers HTTP opcionales
            
        Returns:
            Contenido HTML de la página
            
        Raises:
            RuntimeError: Si no se usa como context manager
            aiohttp.ClientError: Si hay error en la petición
        """
        if not self.session:
            raise RuntimeError("AsyncHTTPClient debe usarse como context manager")
        
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        
        try:
            async with self.session.get(
                url, 
                headers=headers, 
                allow_redirects=True,
                max_redirects=self.max_redirects
            ) as response:
                # Verificar código de estado
                if response.status >= 400:
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=f"HTTP {response.status}",
                        headers=response.headers
                    )
                
                # Verificar tipo de contenido
                content_type = response.headers.get('Content-Type', '').lower()
                if 'text/html' not in content_type and 'text/plain' not in content_type:
                    # Permitir páginas sin Content-Type explícito
                    if content_type and 'application/' in content_type:
                        raise ValueError(f"Tipo de contenido no soportado: {content_type}")
                
                return await response.text(errors='ignore')
                
        except asyncio.TimeoutError:
            raise aiohttp.ClientError(f"Timeout al acceder a {url}")
        except aiohttp.ClientError:
            raise
        except Exception as e:
            raise aiohttp.ClientError(f"Error al acceder a {url}: {str(e)}")
    
    async def fetch_multiple(self, urls, headers=None):
        """
        Realiza múltiples peticiones HTTP en paralelo
        
        Args:
            urls: Lista de URLs a solicitar
            headers: Headers HTTP opcionales
            
        Returns:
            Lista de contenidos (o excepciones si hubo errores)
        """
        if not self.session:
            raise RuntimeError("AsyncHTTPClient debe usarse como context manager")
        
        async def fetch_with_error_handling(url):
            try:
                return await self.fetch(url, headers)
            except Exception as e:
                return e
        
        tasks = [fetch_with_error_handling(url) for url in urls]
        return await asyncio.gather(*tasks)
