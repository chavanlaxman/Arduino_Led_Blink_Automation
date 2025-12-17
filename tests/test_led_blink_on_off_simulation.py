import pytest
import time
from playwright.sync_api import Page, expect
from library.support_method import open_project, press_push_buttons



@pytest.mark.smoke
def test_is_simulation_button_present(wokwi_page):
    """
    This methid will verify is simulation button present
    :param wokwi_page:
    :return:
    """
    page=wokwi_page
    simulation_started=False
    if page.locator("button[aria-label='Start the simulation']").is_visible():
        simulation_started=True
        return simulation_started
    else:
        print("Simulation Green Button not found")
        return simulation_started

@pytest.mark.regression
def test_simulation_led_blink_off_to_on(wokwi_page):
    page=wokwi_page
    print("FIT THE SCREEN FOR MOUSE CLICK ACTION TO PERFORM ON X,Y CO-ORDINATE")
    page.keyboard.press("Shift+KeyF")
    print("CLICK ON START SIMULATION BUTTON")
    page.locator("button[aria-label='Start the simulation']").click()
    print("SIMULATION STARTED")
    press_push_buttons(page, "btn1", hold_ms=500, led_state="ON")
    time.sleep(30)

@pytest.mark.regression
def test_simulation_led_blink_on_to_off(wokwi_page):
    page=wokwi_page
    print("FIT THE SCREEN FOR MOUSE CLICK ACTION TO PERFORM ON X,Y CO-ORDINATE")
    page.keyboard.press("Shift+KeyF")
    print("CLICK ON START SIMULATION BUTTON")
    page.locator("button[aria-label='Start the simulation']").click()
    print("SIMULATION STARTED")
    press_push_buttons(page, "btn1", hold_ms=500, led_state="OFF")
    time.sleep(30)

@pytest.mark.regression
def test_simulation_led_blink_loop(wokwi_page):
    page=wokwi_page
    print("FIT THE SCREEN FOR MOUSE CLICK ACTION TO PERFORM ON X,Y CO-ORDINATE")
    page.keyboard.press("Shift+KeyF")
    print("CLICK ON START SIMULATION BUTTON")
    page.locator("button[aria-label='Start the simulation']").click()
    print("SIMULATION STARTED")
    press_push_buttons(page, "btn1", hold_ms=500)
    time.sleep(30)

