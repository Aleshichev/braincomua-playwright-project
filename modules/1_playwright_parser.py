"""
Parser brain.com.ua using Playwright.
Searches for Apple iPhone 15 128GB Black,
collects complete information about the product, and saves it to a PostgreSQL database.
"""

from load_django import *
from parser_app.models import Product

import random
from time import sleep
import logging
import pandas as pd

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout

# config imports
from config.playwright_config import create_browser_and_context, close_browser
from config.logger_config import setup_logging


# utils imports
# from .utils.collect_products_playwright import collect_product_data
from utils.search_product_plw import search_product, go_to_first_product
def get_url(page: Page, url: str) -> bool:
    for attempt in range(3):
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            logging.info(f"Navigated to URL after {attempt + 1} attempts: {url}")
            sleep(random.uniform(2, 6))
            return True
        except PlaywrightTimeout:
            logging.error(f"Timeout loading URL {url} after {attempt + 1} attempts")
        except Exception as e:
            logging.error(f"Failed to load URL {url} after {attempt + 1} attempts: {e}")

        sleep(random.uniform(1, 4))

    logging.error(f"Failed to load {url} after 3 attempts")
    return False


def save_to_database(product_data: dict):
    """
    Save product data to the database.
    """
    try:
        product = Product.objects.create(**product_data)
        logging.info(f"Product saved to database with ID: {product.id}")
    except Exception as e:
        logging.error(f"Failed to save product to database: {e}")


def export_to_csv():
    """Export all products from the database to a CSV file."""
    try:
        products = Product.objects.all()
        if not products.exists():
            logging.warning("No products found in database to export")
            return

        df = pd.DataFrame(list(products.values()))
        df.to_csv("results/products.csv", index=False)
        logging.info(f"Successfully exported {len(df)} products to CSV")
    except Exception as e:
        logging.error(f"Failed to export products to CSV: {e}")


if __name__ == "__main__":
    logging = setup_logging()

    try:
        # Initialize Playwright headless=True for production
        playwright, browser, context, page = create_browser_and_context(headless=False)

        # Navigate to the main page
        if not get_url(page, "https://brain.com.ua/"):
            raise Exception("Failed to load main page")
        
        if not search_product(page, "Apple iPhone 15 128GB Black"):
            raise Exception("Failed to search for product")

        if not go_to_first_product(page):
            raise Exception("Failed to navigate to first product")
        # product_data = save_to_database(product_data: dict)
        # export_to_csv()

        # Finish parser tasks
        sleep(15)
        close_browser(playwright, browser)
    except Exception as e:
        logging.error(f"An error occurred during parsing: {e}")
