import requests
import pandas as pd
import time
from bs4 import BeautifulSoup

def safe_request(url, headers, proxies=None):
    for attempt in range(3):  # Try 3 times
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=30)  # Increased timeout
            response.raise_for_status()  # Raise an error for bad responses
            response.encoding = response.apparent_encoding  # Set encoding to apparent
            return response
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(f"Skipping invalid URL: {url}")
                return None
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Wait before retrying
        except requests.exceptions.ReadTimeout as e:
            print(f"Read timeout for {url}, attempt {attempt + 1}: {e}")
            time.sleep(2)  # Wait before retrying
    print(f"Failed to retrieve {url} after multiple attempts.")
    return None  # Return None if all attempts fail

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

def scrape_product_data(product_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = safe_request(product_url, headers)
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting product details
        try:
            title = soup.find('h1', class_='product_title').text.strip()
            price = soup.find('span', class_='woocommerce-Price-amount').text.strip()
            image_url = soup.find('img', class_='wp-post-image')['src']
            description = soup.find('div', class_='woocommerce-product-details__short-description').text.strip()
            return {
                'Title': title,
                'Price': price,
                'Image URL': image_url,
                'Description': description,
                'Product URL': product_url
            }
        except Exception as e:
            print(f"Error extracting data from {product_url}: {e}")
    return None

def main():
    # Add the product sitemap of the website to scrap (website-url/product-sitemap)
    sitemap_url = 'https://crosstech.com.ng/product-sitemap.xml'
    product_urls = get_product_urls(sitemap_url)

    total_products = len(product_urls)  # Get the total number of products
    print(f"Total products to scrape: {total_products}\n")

    products = []
    successful_scrapes = 0  # Initialize a counter for successful scrapes
    for url in product_urls:
        print(f"Scraping URL: {url}")
        product_data = scrape_product_data(url)
        if product_data:
            products.append(product_data)
            successful_scrapes += 1  # Increment the counter for successful scrapes
            print(f"Successfully scraped {successful_scrapes}/{total_products} products.")

    # Save to CSV
    df = pd.DataFrame(products)
    df.to_csv('products.csv', index=False, encoding='utf-8', errors='replace')
    print(f"Scraping completed! Data saved to products.csv.")

if __name__ == "__main__":
    main()
