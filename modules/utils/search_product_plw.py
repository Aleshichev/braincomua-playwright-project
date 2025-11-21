"""
Module for searching and navigating to products using Playwright.
"""

import logging
import random
from time import sleep

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeout


def search_product(page: Page, product_name: str) -> bool:
    """
    Search and click on the product using Playwright.
    """
    for attempt in range(3):
        try:
            logging.info(
                f"Searching for product: {product_name}, attempt {attempt + 1}"
            )

            search_input = page.locator(
                "xpath=//div[contains(@class, 'header-bottom-in')]//input[@class='quick-search-input']"
            )

            search_input.wait_for(state="visible", timeout=10000)

            search_input.clear()

            search_input.type(product_name, delay=random.randint(50, 150))

            logging.info(f"Text entered successfully on attempt {attempt + 1}")
            sleep(random.uniform(1, 3))

            search_button = page.locator(
                "xpath=//input[@type='submit' and @class='qsr-submit' and @value='Знайти']"
            )
            search_button.wait_for(state="visible", timeout=10000)
            search_button.click()

            sleep(random.uniform(1, 4))

            logging.info(f"Search completed successfully on attempt {attempt + 1}")
            return True

        except PlaywrightTimeout as e:
            logging.error(f"Timeout error during search (attempt {attempt + 1}): {e}")
            sleep(2)
        except Exception as e:
            logging.error(f"Search error (attempt {attempt + 1}): {e}")
            sleep(2)

    logging.error("Search product failed after 3 retries")
    return False


def go_to_first_product(page: Page) -> bool:
    """
    Navigate to the first product from search results.
    """
    for attempt in range(3):
        try:
            logging.info(f"Navigating to first product, attempt {attempt + 1}")

            first_product = page.locator('xpath=//div[@data-stock="1"][1]//a').first
            # first_product = page.locator('xpath=//div[@data-stock="1"]//a').first

            first_product.wait_for(state="visible", timeout=5000)

            first_product.click()

            page.wait_for_load_state("domcontentloaded")
            sleep(random.uniform(2, 5))

            logging.info(
                f"Navigated to first product successfully on attempt {attempt + 1}"
            )
            return True

        except PlaywrightTimeout as e:
            logging.error(
                f"Timeout error navigating to product (attempt {attempt + 1}): {e}"
            )
            sleep(2)
        except Exception as e:
            logging.error(
                f"Navigation error to first product (attempt {attempt + 1}): {e}"
            )
            sleep(2)

    logging.error("Navigation to first product failed after 3 retries")
    return False
