"""
Parser brain.com.ua using Playwright.
Searches for Apple iPhone 15 128GB Black,
collects complete information about the product, and saves it to a PostgreSQL database.
"""

from time import sleep

from config.logger_config import setup_logging
# config imports
from config.playwright_config import close_browser, create_browser_and_context
from load_django import *
# utils imports
from utils.collect_products_plw import collect_product_data
from utils.get_main_url import get_url
from utils.search_product_plw import go_to_first_product, search_product
from utils.storage import export_to_csv, save_to_database


def main():
    logging = setup_logging()

    try:
        # Initialize Playwright headless=True for production
        playwright, browser, context, page = create_browser_and_context(headless=True)

        # Navigate to the main page
        if not get_url(page, "https://brain.com.ua/"):
            raise Exception("Failed to load main page")

        if not search_product(page, "Apple iPhone 15 128GB Black"):
            raise Exception("Failed to search for product")

        if not go_to_first_product(page):
            raise Exception("Failed to navigate to first product")

        product_data = collect_product_data(page)
        sleep(15)
        close_browser(playwright, browser)

        if product_data:
            save_to_database(product_data)
            export_to_csv()

        logging.info("Parsing completed successfully")

    except Exception as e:
        logging.error(f"An error occurred during parsing: {e}")


if __name__ == "__main__":
    main()
