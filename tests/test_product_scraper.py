import unittest
from unittest.mock import patch
from types import SimpleNamespace

from scraper.product_scraper import scrape_product_data


class ProductScraperTests(unittest.TestCase):
    @patch("scraper.product_scraper.safe_request")
    def test_does_not_assume_catalogue_state_when_markup_is_missing(self, request):
        request.return_value = SimpleNamespace(content=b"""
            <html><h1 class="product_title">Sample item</h1>
            <div class="summary"><p class="price"><span class="amount">$20.00</span></p></div>
            </html>
        """)
        product = scrape_product_data("https://shop.example/product/sample")
        self.assertEqual(product["Name"], "Sample item")
        self.assertIsNone(product["Published"])
        self.assertIsNone(product["Visibility in catalog"])
        self.assertIsNone(product["In stock?"])
        self.assertIsNone(product["Backorders allowed?"])
        self.assertEqual(product["Regular price"], "$20.00")

    @patch("scraper.product_scraper.safe_request")
    def test_extracts_stock_state_and_gallery_images(self, request):
        request.return_value = SimpleNamespace(content=b"""
            <html><h1 class="product_title">Available item</h1>
            <p class="stock in-stock">In stock</p>
            <div class="woocommerce-product-gallery__image">
              <img src="https://cdn.example/item.jpg">
            </div></html>
        """)
        product = scrape_product_data("https://shop.example/product/available")
        self.assertEqual(product["In stock?"], 1)
        self.assertIn("item.jpg", product["Images"])

    def test_rejects_non_http_urls(self):
        with self.assertRaises(ValueError):
            scrape_product_data("file:///etc/passwd")


if __name__ == "__main__":
    unittest.main()
