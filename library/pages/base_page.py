"""
Base Page Object Model
Contains common methods and locator patterns used across all page objects
"""
from playwright.sync_api import Page
import time


class BasePage:
    """Base class for all page objects"""

    def __init__(self, page: Page):
        self.page = page

    def wait_for_url(self, url: str, timeout: int = 120000):
        """Wait for page to load with specific URL"""
        self.page.wait_for_url(url, timeout=timeout)
        print(f"Successfully navigated to {url}")

    def is_element_visible(self, locator: str) -> bool:
        """Check if element is visible"""
        try:
            return self.page.locator(locator).is_visible(timeout=5000)
        except:
            return False

    def wait_for_element(self, locator: str, timeout: int = 10000, state: str = "visible"):
        """Wait for element to be in specific state"""
        self.page.locator(locator).wait_for(state=state, timeout=timeout)

    def take_screenshot(self, filename: str):
        """Take screenshot and save with given filename"""
        self.page.screenshot(path=filename)

    def wait_and_sleep(self, seconds: int = 3):
        """Wait for specified seconds"""
        time.sleep(seconds)

    def get_text_from_locator(self, locator: str) -> str:
        """Get text content from element"""
        return self.page.locator(locator).inner_text()

    def get_input_value(self, locator: str) -> str:
        """Get input value from element"""
        return self.page.locator(locator).input_value()

    def fill_input(self, locator: str, value: str):
        """Fill input field with value"""
        self.page.locator(locator).fill(str(value))

    def click_element(self, locator: str, force: bool = False):
        """Click on element"""
        self.page.locator(locator).click(force=force)

    def evaluate_js(self, script: str):
        """Evaluate JavaScript on the page"""
        return self.page.evaluate(script)

    def press_key(self, key_combination: str):
        """Press keyboard key combination"""
        self.page.keyboard.press(key_combination)
