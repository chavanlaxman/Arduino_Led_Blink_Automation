import pytest
from playwright.sync_api import Page, Playwright

from library.framewrok_url import PROJECT_URL
from library.support_method import open_project


@pytest.fixture(scope='session')
def launch_browser_chromium(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    yield page
    page.close()
    context.close()
    browser.close()

@pytest.fixture
def wokwi_page(launch_browser_chromium):
    wokwi_page = launch_browser_chromium
    open_project(wokwi_page, PROJECT_URL)
    return wokwi_page


