"""
Playwright browser configuration with anti-detection settings.
"""

from playwright.sync_api import sync_playwright
import logging


def get_browser_args() -> list:
    """
    Get browser launch arguments for anti-detection.

    Returns:
        List of browser arguments
    """
    return [
        "--disable-blink-features=AutomationControlled",
        "--disable-dev-shm-usage",
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-popup-blocking",
        "--disable-notifications",
    ]


def get_context_options() -> dict:
    """
    Get browser context options for stealth mode.

    Returns:
        Dictionary with context options
    """
    return {
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "locale": "uk-UA",
        "timezone_id": "Europe/Kiev",
        "permissions": [],
        "geolocation": None,
        "extra_http_headers": {
            "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
        },
    }


def create_browser_and_context(headless: bool):
    """
    Create Playwright browser and context with anti-detection settings.

    Args:
        headless: Run browser in headless mode

    Returns:
        Tuple of (playwright, browser, context, page)
    """
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=headless,
        args=get_browser_args(),
        slow_mo=50,  # Sloqw down operations by 50ms
    )

    context = browser.new_context(**get_context_options())

    # Script to evade detection
    context.add_init_script(
        """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        
        Object.defineProperty(navigator, 'languages', {
            get: () => ['uk-UA', 'uk', 'en-US', 'en']
        });
        
        // Chrome property
        window.chrome = {
            runtime: {}
        };
        
        // Permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
    """
    )

    page = context.new_page()

    logging.info("Playwright browser and context created successfully")

    return playwright, browser, context, page


def close_browser(playwright, browser):
    """
    Close browser and playwright instance.

    Args:
        playwright: Playwright instance
        browser: Browser instance
    """
    try:
        if browser:
            browser.close()
        if playwright:
            playwright.stop()
        logging.info("Browser closed successfully")
    except Exception as e:
        logging.error(f"Error closing browser: {e}")
