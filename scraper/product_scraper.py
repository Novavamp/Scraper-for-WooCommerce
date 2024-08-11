from bs4 import BeautifulSoup  # Importing BeautifulSoup for parsing HTML content
from .request_utils import safe_request  # Importing a custom function for making safe HTTP requests
from .html_utils import clean_html  # Importing a custom function to clean and process HTML content

def scrape_product_data(product_url):
    # Define HTTP headers to simulate a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Make a safe HTTP GET request to the product URL
    response = safe_request(product_url, headers)
    
    # If the request is successful, parse the HTML content
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            # Extract product images
            images = []
            image_elements = soup.select('div.woocommerce-product-gallery__image img')
            for img in image_elements:
                if 'src' in img.attrs:
                    images.append(img['src'])

            # Join image URLs into a single string, or set to None if no images are found
            image_urls = ', '.join(images) if images else None

            # Extract and clean the short description
            short_description_element = soup.select_one('.product-section .woocommerce-product-details__short-description')
            short_description_html = clean_html(short_description_element.decode_contents().strip(), max_words=30) if short_description_element else None
            
            # Extract and clean the full description, retaining certain HTML tags
            description_element = soup.select_one('.woocommerce-tabs .panel.entry-content')
            description_html = clean_html(description_element.decode_contents().strip(), retain_h2=True) if description_element else None
            
            # Compile the product data into a dictionary
            product_data = {
                'Name': soup.find('h1', class_='product_title').text.strip() if soup.find('h1', class_='product_title') else None,
                'Published': 1,  # Assume the product is published
                'Visibility in catalog': 'visible',  # Set product visibility to 'visible'
                'Short description': short_description_html,
                'Description': description_html,
                'In stock?': 1,  # Assume the product is in stock
                'Backorders allowed?': 0,  # Assume backorders are not allowed
                'Weight': 0,  # Default weight value, can be updated if weight information is available
                'Allow customer reviews?': 1,  # Assume customer reviews are allowed
                'Sale price': soup.find('span', class_='woocommerce-Price-amount amount').text.strip() if soup.find('span', class_='woocommerce-Price-amount amount') else None,
                'Regular price': soup.find('span', class_='woocommerce-Price-amount amount').text.strip() if soup.find('span', class_='woocommerce-Price-amount amount') else None,
                'Categories': ', '.join([cat.text.strip() for cat in soup.find_all('a', rel='tag')]) if soup.find_all('a', rel='tag') else None,
                'Tags': None,  # Tags can be updated if information is available
                'Images': image_urls,
                'Position': 0,  # Default position value
                'Product URL': product_url
            }

            # Return the compiled product data
            return product_data

        except Exception as e:
            # Print an error message if data extraction fails
            print(f"Error extracting data from {product_url}: {e}")
    
    # Return None if the request fails or data extraction encounters an error
    return None
