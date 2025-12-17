from playwright.sync_api import  Page

from library.framewrok_url import PROJECT_URL


def test_playwright_example(page: Page):
    url = "https://wokwi.com/projects/450024899014635521"
    page.goto(PROJECT_URL)
