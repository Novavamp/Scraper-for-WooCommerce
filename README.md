```markdown
#WooCommerce Product Scraper

This Python script scrapes product data from a WooCommerce website using its sitemap. It retrieves
product details such as name, description, images, prices, and more, and saves the data in a CSV file.

##Features

- Fetches product URLs from the provided sitemap.
- Handles HTTP errors and timeouts with retries.
- Extracts essential product information, including:
  - Product name
  - Short description
  - Detailed description
  - Sale price
  - Regular price
  - Categories
  - Image URLs
- Saves the scraped data to a CSV file.

## Requirements

- Python 3.x
- `requests` library
- `pandas` library
- `beautifulsoup4` library

You can install the required libraries using pip:

```bash
pip install requests pandas beautifulsoup4
```

## Usage

1. Clone this repository:

   ```bash
   git clone https://github.com/novavamp/product-scraper.git
   cd product-scraper
   ```

2. Update the `sitemap_url` variable in the `main()` function with the URL of the sitemap you want to scrape.

3. Run the script:

   ```bash
   python product_scraper.py
   ```

4. The scraped data will be saved in a file named `products.csv`.

## Notes

- Make sure to comply with the website's `robots.txt` and scraping policies.
- This script is designed for educational purposes and should be used responsibly.
- If you encounter issues, ensure that the CSS selectors used in the script match the structure of the target website.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
