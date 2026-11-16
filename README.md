# WooCommerce Product Data Scraper

A Python utility that reads product pages from WooCommerce-powered websites and maps selected product information into a dictionary suitable for further processing or CSV export.

## Features

- Retrieve product pages with request timeouts and retry attempts.
- Parse product titles, descriptions, images, prices, and taxonomy labels.
- Clean HTML descriptions for downstream catalogue imports.
- Read product URLs from XML sitemaps.

## Stack

- Python
- Requests
- Beautiful Soup
- Beautiful Soup XML parsing

## Setup

```bash
git clone https://github.com/Novavamp/Scraper-for-WooCommerce.git
cd Scraper-for-WooCommerce
python -m venv .venv
```

Activate the virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

## Current limitations

WooCommerce themes and plugins can change the markup used for product data. The current scraper relies on common WooCommerce CSS selectors and should be validated against each target site.

Some import fields in the current implementation are defaults rather than values verified from the source page. In particular, publication state, catalogue visibility, stock state, backorders, weight, and customer-review settings should not be assumed for a real catalogue. Review and correct these values before importing the generated data.

The request helper currently retries selected HTTP and timeout failures. It should be extended to handle connection errors and other transient failures consistently, and to use server-provided retry guidance where appropriate.

## Responsible use

Only collect product information where you have permission. Respect website terms, robots guidance, request limits, and applicable laws. Avoid collecting personal information.

## Project structure

- `main.py` — application entry point.
- `scraper/product_scraper.py` — product-page extraction.
- `scraper/request_utils.py` — HTTP request helper.
- `scraper/html_utils.py` — description cleanup.
- `scraper/sitemap_utils.py` — sitemap URL extraction.
