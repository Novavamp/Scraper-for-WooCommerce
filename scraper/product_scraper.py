from urllib.parse import urlparse

from bs4 import BeautifulSoup

from .request_utils import safe_request
from .html_utils import clean_html


def _text(soup, selectors):
    for selector in selectors:
        node = soup.select_one(selector)
        if node:
            value = node.get_text(" ", strip=True)
            if value:
                return value
    return None


def _attribute(soup, selectors, attribute):
    for selector in selectors:
        node = soup.select_one(selector)
        if node and node.get(attribute):
            return node.get(attribute).strip()
    return None


def scrape_product_data(product_url, *, request_options=None):
    """Extract product data from a WooCommerce product page.

    Import-sensitive fields remain unset when the source page does not expose
    a reliable value. Callers can pass request options such as headers/proxies.
    """
    parsed = urlparse(product_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("product_url must be an absolute HTTP(S) URL")

    response = safe_request(product_url, **(request_options or {}))
    if response is None:
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    title = _text(soup, ["h1.product_title", "h1.entry-title"])
    if not title:
        return None

    image_urls = []
    for image in soup.select(
        ".woocommerce-product-gallery__image img, "
        ".woocommerce-product-gallery img, img.wp-post-image"
    ):
        src = image.get("data-src") or image.get("data-large_image") or image.get("src")
        if src and src not in image_urls:
            image_urls.append(src)

    short_node = soup.select_one(
        ".product-section .woocommerce-product-details__short-description, "
        ".woocommerce-product-details__short-description"
    )
    full_node = soup.select_one(
        ".woocommerce-tabs .panel.entry-content, "
        "#tab-description, .woocommerce-Tabs-panel--description"
    )
    short_description = (
        clean_html(short_node.decode_contents().strip(), max_words=30)
        if short_node else None
    )
    description = (
        clean_html(full_node.decode_contents().strip(), retain_h2=True)
        if full_node else None
    )

    regular_price = _attribute(
        soup,
        ["del .woocommerce-Price-amount", ".summary del .amount"],
        "data-price",
    ) or _text(soup, ["del .woocommerce-Price-amount", ".summary del .amount"])

    sale_price = _attribute(
        soup,
        ["ins .woocommerce-Price-amount", ".summary ins .amount"],
        "data-price",
    ) or _text(soup, ["ins .woocommerce-Price-amount", ".summary ins .amount"])

    if not regular_price and not sale_price:
        current_price = _text(soup, [".summary .price .woocommerce-Price-amount", ".summary .price"])
        regular_price = current_price

    stock_node = soup.select_one(".stock")
    stock_text = stock_node.get_text(" ", strip=True).lower() if stock_node else ""
    stock_value = None
    if stock_node and ("out of stock" in stock_text):
        stock_value = 0
    elif stock_node and ("in stock" in stock_text):
        stock_value = 1

    weight = _text(soup, [".product_weight", ".woocommerce-product-attributes-item--weight .woocommerce-product-attributes-item__value"])
    categories = [
        item.get_text(" ", strip=True)
        for item in soup.select(".posted_in a, .product_meta .posted_in a")
        if item.get_text(" ", strip=True)
    ]
    tags = [
        item.get_text(" ", strip=True)
        for item in soup.select(".tagged_as a, .product_meta .tagged_as a")
        if item.get_text(" ", strip=True)
    ]

    return {
        "Name": title,
        "Published": None,
        "Visibility in catalog": None,
        "Short description": short_description,
        "Description": description,
        "In stock?": stock_value,
        "Backorders allowed?": None,
        "Weight": weight,
        "Allow customer reviews?": None,
        "Sale price": sale_price,
        "Regular price": regular_price,
        "Categories": ", ".join(categories) if categories else None,
        "Tags": ", ".join(tags) if tags else None,
        "Images": ", ".join(image_urls) if image_urls else None,
        "Position": 0,
        "Product URL": product_url,
    }
