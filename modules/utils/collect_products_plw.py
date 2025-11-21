"""
Module for collecting product data using Playwright.
"""

import random
from time import sleep
import logging
import re
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout


def clean_text(text):
    """Clean and normalize text."""
    if not text:
        return text
    return text.replace("\xa0", " ").strip()


def get_product_title(page: Page) -> str:
    """
    Extract product title.
    """
    try:
        title = page.locator(
            "xpath=//div[@class='main-right-block ']//h1[@class='desktop-only-title']"
        ).first
        title.wait_for(state="visible", timeout=10000)
        title_text = title.inner_text().strip()
        logging.info(f"Product title found: {title_text}")
        return title_text
    except PlaywrightTimeout:
        logging.error("Product title not found - timeout")
        return None
    except Exception as e:
        logging.error(f"Product title not found: {e}")
        return None


def get_product_price(page: Page) -> float:
    """
    Extract product regular price.
    """
    try:
        price_element = page.locator(
            "xpath=//div[@class='br-pr-price main-price-block']//div[@class='price-wrapper']"
        ).first
        price_element.wait_for(state="visible", timeout=10000)

        price_text = price_element.inner_text().strip().replace("\n", "")
        price = re.sub(r"[^\d.]", "", price_text)
        price = price.replace(",", ".")
        price_float = float(price)

        logging.info(f"Price found: {price_float}")
        return price_float
    except PlaywrightTimeout:
        logging.error("Price not found - timeout")
        return None
    except Exception as e:
        logging.error(f"Price not found: {e}")
        return None


def get_product_photos(page: Page) -> list:
    """
    Extract all product photos.
    """
    try:
        photo_elements = page.locator(
            "xpath=//div[@class='product-block-right']//div[@class='slick-track']//img"
        ).all()

        if not photo_elements:
            logging.info("No photos found")
            return []

        photos = []
        for img in photo_elements:
            src = img.get_attribute("src")
            if src:
                photos.append(src)

        logging.info(f"Added {len(photos)} photos")
        return photos
    except Exception as e:
        logging.error(f"Error getting photos: {e}")
        return []


def get_review_count(page: Page) -> int:
    """
    Extract review count.
    """
    try:
        review_element = page.locator(
            "xpath=//div[@class='title']//a[@class='forbid-click reviews-count']//span"
        ).first
        review_element.wait_for(state="visible", timeout=10000)

        count = int(review_element.inner_text().strip())
        logging.info(f"Review count found: {count}")
        return count
    except PlaywrightTimeout:
        logging.error("Review count not found - timeout")
        return None
    except Exception as e:
        logging.error(f"Review count not found: {e}")
        return None


def get_product_code(page: Page) -> str:
    """
    Extract product code.
    """
    try:
        code_element = page.locator(
            "xpath=//div[@class='title']//span[@class='br-pr-code-val']"
        ).first
        code_element.wait_for(state="visible", timeout=10000)

        code_text = code_element.inner_text().strip()
        logging.info(f"Product code found: {code_text}")
        return code_text
    except PlaywrightTimeout:
        logging.error("Product code not found - timeout")
        return None
    except Exception as e:
        logging.error(f"Product code not found: {e}")
        return None


def scroll_to_characteristics(page: Page):
    """
    Scroll down to characteristics section.
    """
    try:
        page.mouse.wheel(0, 700)
        sleep(random.uniform(2, 5))
        logging.info("Scrolled 700px down")
    except Exception as e:
        logging.warning(f"Scroll error, trying alternative: {e}")
        try:
            page.mouse.wheel(0, 1000)
            sleep(random.uniform(1, 4))
            logging.info("Scrolled 1000px down")
        except Exception as e2:
            logging.error(f"Scroll failed: {e2}")


def expand_all_characteristics(page: Page) -> bool:
    """
    Click button to show all characteristics.
    """
    try:
        button = page.locator(
            "xpath=//div[@id='br-characteristics']//button[@class='br-prs-button']"
        ).first

        button.wait_for(state="visible", timeout=10000)
        button.click()

        sleep(random.uniform(2, 5))
        logging.info("Clicked 'show all characteristics' button")
        return True
    except PlaywrightTimeout:
        logging.error("Characteristics button not found - timeout")
        return False
    except Exception as e:
        logging.error(f"Navigation error to all characteristics: {e}")
        return False


def scroll_after_expand(page: Page):
    """
    Scroll down after expanding characteristics.
    """
    try:
        page.mouse.wheel(0, 1000)
        sleep(random.uniform(2, 5))
        logging.info("Scrolled 1000px down after expand")
    except Exception as e:
        logging.warning(f"Scroll error, trying alternative: {e}")
        try:
            page.mouse.wheel(0, 1500)
            sleep(random.uniform(1, 4))
            logging.info("Scrolled 1500px down after expand")
        except Exception as e2:
            logging.error(f"Scroll failed: {e2}")


def parse_specification_row(row) -> tuple:
    """
    Parse a single specification row to extract key-value pair.
    """
    try:
        spans = row.locator("xpath=//span").all()
        if len(spans) < 2:
            return None, None

        key = spans[0].inner_text().strip()
        values = []

        for span in spans[1:]:
            # Check for links inside the span
            links = span.locator("xpath=//a").all()
            if links:
                values.extend([link.inner_text().strip() for link in links])
            else:
                text = span.inner_text().strip()
                if text:
                    values.append(text)

        value = ", ".join(values) if values else None
        return key, value
    except Exception as e:
        logging.warning(f"Error parsing specification row: {e}")
        return None, None


def parse_specification_detail(detail) -> dict:
    """
    Parse a single specification detail block.

    """
    specs = {}
    try:
        title_element = detail.locator("xpath=//h3").first
        title_section = title_element.inner_text().strip()
        specs[title_section] = {}

        rows = detail.locator("xpath=//div").all()
        for row in rows:
            key, value = parse_specification_row(row)
            if key:
                specs[title_section][key] = clean_text(value)

        return specs
    except Exception as e:
        logging.warning(f"Section title (h3) not found in detail block: {e}")
        return {}


def get_product_specifications(page: Page) -> dict:
    """
    Extract all product specifications.
    """
    try:
        specifications = page.locator(
            "xpath=//div[@class='br-wrap-block br-elem-block']"
        ).all()

        if not specifications:
            logging.error("Specifications not found")
            return {}

        specs_dict = {}
        for spec in specifications:
            try:
                details = spec.locator("xpath=//div[@class='br-pr-chr-item']").all()
                for detail in details:
                    detail_specs = parse_specification_detail(detail)
                    specs_dict.update(detail_specs)

                logging.info("Collected details for specification section")
            except Exception as e:
                logging.error(f"Specification details error: {e}")
                continue

        logging.info(f"Collected {len(specs_dict)} specification sections")
        return specs_dict

    except Exception as e:
        logging.error(f"Specifications not found: {e}")
        return {}


def extract_specific_specs(specifications: dict) -> dict:
    """
    Extract specific specifications from the full specs dictionary.
    """
    specific_data = {}

    try:
        specific_data["manufacturer"] = specifications.get("Інші", {}).get("Виробник")
    except Exception as e:
        logging.warning(f"Could not extract manufacturer: {e}")
        specific_data["manufacturer"] = None

    try:
        specific_data["memory"] = specifications.get("Функції пам'яті", {}).get(
            "Вбудована пам'ять"
        )
    except Exception as e:
        logging.warning(f"Could not extract memory: {e}")
        specific_data["memory"] = None

    try:
        specific_data["color"] = specifications.get("Фізичні характеристики", {}).get(
            "Колір"
        )
    except Exception as e:
        logging.warning(f"Could not extract color: {e}")
        specific_data["color"] = None

    try:
        specific_data["screen_diagonal"] = specifications.get("Дисплей", {}).get(
            "Діагональ екрану"
        )
    except Exception as e:
        logging.warning(f"Could not extract screen diagonal: {e}")
        specific_data["screen_diagonal"] = None

    try:
        specific_data["screen_resolution"] = specifications.get("Дисплей", {}).get(
            "Роздільна здатність екрану"
        )
    except Exception as e:
        logging.warning(f"Could not extract screen resolution: {e}")
        specific_data["screen_resolution"] = None

    return specific_data


def collect_product_data(page: Page) -> dict:
    """
    Collect product data from the product page.
    """
    logging.info("Start collecting product data...")

    product_data = {}

    # Basic product information
    product_data["title"] = get_product_title(page)
    product_data["regular_price"] = get_product_price(page)
    product_data["sale_price"] = None
    product_data["photos"] = get_product_photos(page)
    product_data["review_count"] = get_review_count(page)
    product_data["code"] = get_product_code(page)

    # Scroll and expand characteristics
    scroll_to_characteristics(page)
    expand_all_characteristics(page)
    scroll_after_expand(page)

    # Collect specifications
    product_data["specifications"] = get_product_specifications(page)

    # Extract specific specifications
    specific_specs = extract_specific_specs(product_data["specifications"])
    product_data.update(specific_specs)

    print(product_data)
    return product_data
