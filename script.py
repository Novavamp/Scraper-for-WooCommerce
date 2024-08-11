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
            images = []
            image_elements = soup.select('div.woocommerce-product-gallery__image img')
            for img in image_elements:
                if 'src' in img.attrs:
                    images.append(img['src'])

            image_urls = ', '.join(images) if images else None
            
            product_data = {
                'Name': soup.find('h1', class_='product_title').text.strip() if soup.find('h1', class_='product_title') else None,
                'Published': 1,
                'Visibility in catalog': 'visible',
                'Short description': soup.select_one('.product-section .woocommerce-product-details__short-description').get_text(separator='\n').strip() if soup.select_one('.product-section .woocommerce-product-details__short-description') else None,
                'Description': soup.select_one('.woocommerce-tabs .panel.entry-content').get_text(separator='\n').strip() if soup.select_one('.woocommerce-tabs .panel.entry-content') else None,  # Ensure this selector is correct
                'In stock?': 1,
                'Backorders allowed?': 0,
                'Weight': 0,  # Update if weight information is available
                'Allow customer reviews?': 1,
                'Sale price': soup.find('span', class_='woocommerce-Price-amount amount').text.strip() if soup.find('span', class_='woocommerce-Price-amount amount') else None,
                'Regular price': soup.find('span', class_='woocommerce-Price-amount amount').text.strip() if soup.find('span', class_='woocommerce-Price-amount amount') else None,
                'Categories': ', '.join([cat.text.strip() for cat in soup.find_all('a', rel='tag')]) if soup.find_all('a', rel='tag') else None,
                'Tags': None,  # Update if tags information is available
                'Images': image_urls,
                'Position': 0,
                'Product URL': product_url
            }

            return product_data

        except Exception as e:
            print(f"Error extracting data from {product_url}: {e}")
    return None

def main():
    sitemap_url = 'https://crosstech.com.ng/product-sitemap.xml'
    product_urls = get_product_urls(sitemap_url)
    
    total_products = len(product_urls)
    print(f"Total products to scrape: {total_products}")
    
    products = []
    for index, url in enumerate(product_urls, start=1):
        print(f"Scraping {index}/{total_products} URL: {url}")
        product_data = scrape_product_data(url)
        if product_data:
            products.append(product_data)

    # Save to CSV
    df = pd.DataFrame(products)
    df.to_csv('products.csv', index=False, encoding='utf-8', errors='replace')
    print(f"Scraping completed! Data saved to products.csv.")

if __name__ == "__main__":
    main()
