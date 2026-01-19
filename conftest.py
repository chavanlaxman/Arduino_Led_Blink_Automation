import pytest
from playwright.sync_api import Page, Playwright
from library.framewrok_url import TEMP_HUMI_SESNOR_URL, LED_BLINK_PROJECT_URL
from library.support_method import open_project

def pytest_addoption(parser):
    parser.addoption("--project", action="store", default="led", help="Choose project: sensor or led")

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
def get_project_url(request):
    project = request.config.getoption("--project")
    print(f"===========STARTING PROJECT {project.upper()} ================== ")
    if project == "sensor":
        return TEMP_HUMI_SESNOR_URL
    return LED_BLINK_PROJECT_URL
@pytest.fixture
def wokwi_page(launch_browser_chromium, get_project_url):
    wokwi_page = launch_browser_chromium
    open_project(wokwi_page, get_project_url)
    return wokwi_page


