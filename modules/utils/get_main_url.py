import logging
import random
from time import sleep

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeout


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
