import pandas as pd
from scraper.sitemap_utils import get_product_urls
from scraper.product_scraper import scrape_product_data

def main():
    sitemap_url = 'your-url/product-sitemap.xml' #Enter the Sitemap URL here
    product_urls = get_product_urls(sitemap_url)
    
    total_products = len(product_urls)
    print(f"Total products to scrape: {total_products}")
    
    products = []
    for index, url in enumerate(product_urls, start=1):
        print(f"Scraping {index}/{total_products} URL: {url}")
        product_data = scrape_product_data(url)
        if product_data:
            products.append(product_data)

    df = pd.DataFrame(products)
    df.to_csv('products.csv', index=False, encoding='utf-8', errors='replace')
    print(f"Scraping completed! Data saved to products.csv.")

if __name__ == "__main__":
    main()
