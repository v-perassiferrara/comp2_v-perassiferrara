import argparse
import asyncio
import aiohttp.web
import datetime
import os
import sys

# Add the project root to the sys.path to allow imports from common and scraper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.protocol import Protocol
from common.serialization import serialize, deserialize
from scraper.html_parser import HTMLParser
from scraper.metadata_extractor import MetadataExtractor
from scraper.async_http import AsyncHTTPClient


# Configuration for the processing server
PROCESSING_SERVER_IP = '127.0.0.1' # Default, can be configured via env var or CLI if needed
PROCESSING_SERVER_PORT = 8001 # Default, can be configured

async def connect_to_processing_server():
    """Establishes an asynchronous connection to the processing server."""
    try:
        reader, writer = await asyncio.open_connection(PROCESSING_SERVER_IP, PROCESSING_SERVER_PORT)
        return reader, writer
    except Exception as e:
        print(f"Error connecting to processing server: {e}")
        return None, None

async def handle_scrape(request):
    url = request.query.get('url')
    if not url:
        return aiohttp.web.json_response({'status': 'error', 'message': 'Missing URL parameter'}, status=400)

    print(f"Scraping request received for URL: {url}")

    http_client = AsyncHTTPClient()
    scraping_data = {}
    processing_data = {}
    status = 'success'
    error_message = None

    try:
        html_content = await http_client.fetch(url)
        soup = HTMLParser.parse_html(html_content)

        scraping_data = {
            'title': HTMLParser.extract_title(soup),
            'links': HTMLParser.extract_links(soup, url),
            'meta_tags': MetadataExtractor.extract_all_metadata(soup),
            'structure': HTMLParser.extract_structure(soup),
            'images_count': HTMLParser.count_images(soup)
        }

        # Communicate with processing server
        reader, writer = await connect_to_processing_server()
        if reader and writer:
            processing_request = {'url': url}
            await Protocol.send_async(writer, processing_request)
            processing_response = await Protocol.receive_async(reader)
            writer.close()
            await writer.wait_closed()

            if processing_response.get('status') == 'success':
                processing_data = processing_response.get('processing_data', {})
            else:
                status = 'warning'
                error_message = f"Processing server error: {processing_response.get('message', 'Unknown error')}"
                print(error_message)
        else:
            status = 'warning'
            error_message = "Could not connect to processing server."
            print(error_message)

    except asyncio.TimeoutError:
        status = 'error'
        error_message = "Scraping timed out."
        print(f"Scraping timed out for URL: {url}")
    except Exception as e:
        status = 'error'
        error_message = str(e)
        print(f"Error scraping URL {url}: {e}")

    response_payload = {
        "url": url,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scraping_data": scraping_data,
        "processing_data": processing_data,
        "status": status
    }
    if error_message:
        response_payload['error'] = error_message

    return aiohttp.web.json_response(response_payload)

async def main():
    global PROCESSING_SERVER_IP, PROCESSING_SERVER_PORT
    parser = argparse.ArgumentParser(description="Servidor de Scraping Web Asíncrono")
    parser.add_argument('-i', '--ip', type=str, required=True, help="Dirección de escucha (soporta IPv4/IPv6)")
    parser.add_argument('-p', '--port', type=int, required=True, help="Puerto de escucha")
    parser.add_argument('-w', '--workers', type=int, default=4, help="Número de workers (default: 4)")
    parser.add_argument('--processing_ip', type=str, default=PROCESSING_SERVER_IP,
                        help=f"IP del servidor de procesamiento (default: {PROCESSING_SERVER_IP})")
    parser.add_argument('--processing_port', type=int, default=PROCESSING_SERVER_PORT,
                        help=f"Puerto del servidor de procesamiento (default: {PROCESSING_SERVER_PORT})")

    args = parser.parse_args()

    PROCESSING_SERVER_IP = args.processing_ip
    PROCESSING_SERVER_PORT = args.processing_port

    app = aiohttp.web.Application()
    app.router.add_get('/scrape', handle_scrape)

    print(f"Servidor de Scraping escuchando en {args.ip}:{args.port} (Processing server: {PROCESSING_SERVER_IP}:{PROCESSING_SERVER_PORT})")
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, args.ip, args.port)
    await site.start()

    # Keep the server running indefinitely
    while True:
        await asyncio.sleep(3600) # Sleep for an hour, or use a more robust shutdown mechanism

if __name__ == '__main__':
    asyncio.run(main())
