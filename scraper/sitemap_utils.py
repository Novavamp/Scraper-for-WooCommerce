from bs4 import BeautifulSoup
from .request_utils import safe_request

def get_product_urls(sitemap_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = safe_request(sitemap_url, headers)
    if response:
        soup = BeautifulSoup(response.content, 'xml')
        urls = [url.loc.text for url in soup.find_all('url')]
        return urls
    return []
