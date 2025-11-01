import argparse
import aiohttp
import asyncio
import json

# Direccion predeterminada del servidor
SCRAPING_SERVER_IP = '127.0.0.1'
SCRAPING_SERVER_PORT = 8000

async def fetch_and_display_results(url, server_ip, server_port):
    scrape_url = f"http://{server_ip}:{server_port}/scrape?url={url}"
    print(f"Solicitando scraping para: {url}")
    print(f"A través del servidor: {scrape_url}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(scrape_url) as response:
                response.raise_for_status()  # Lanzar excepcion por errores HTTP (4xx o 5xx)
                data = await response.json()
                print("\n--- Resultados de Scraping y Procesamiento ---")
                print(json.dumps(data, indent=2))
    except aiohttp.ClientError as e:
        print(f"Error al conectarse al servidor de scraping o durante la solicitud: {e}")
    except json.JSONDecodeError:
        print("Error: No se pudo decodificar la respuesta JSON del servidor.")
    except Exception as e:
        print(f"Ocurrio un error inesperado: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Cliente para el Sistema de Scraping Web Distribuido")
    parser.add_argument('--url', type=str, required=True, help="URL a scrapear y analizar")
    parser.add_argument('--server_ip', type=str, default=SCRAPING_SERVER_IP,
                        help=f"IP del servidor de scraping (default: {SCRAPING_SERVER_IP})")
    parser.add_argument('--server_port', type=int, default=SCRAPING_SERVER_PORT,
                        help=f"Puerto del servidor de scraping (default: {SCRAPING_SERVER_PORT})")

    args = parser.parse_args()

    await fetch_and_display_results(args.url, args.server_ip, args.server_port)

if __name__ == '__main__':
    asyncio.run(main())
