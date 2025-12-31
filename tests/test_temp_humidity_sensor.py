import pytest
from playwright.sync_api import Page
from library.support_method import read_monitor, click_on_sensor
import time
import re


@pytest.mark.sensor
def test_system_startup(wokwi_page):
    """
    This method will verify arduino Uno
    :param page:
    :return:
    """
    page = wokwi_page
    print("CLICK ON START SIMULATION BUTTON")
    page.locator("button[aria-label='Start the simulation']").click()
    print("GET CONSOLE OUTPUT")
    text = read_monitor(page)
    assert 'SYSTEM_STARTED' in text, "Arduino simulator not started"
    return text



def get_serial_text(page):
    return page.locator("textarea").input_value()


def set_temperature(page, value):
    temp_slider = page.locator('input[type="range"]').nth(0)
    temp_slider.fill(str(value))


def set_humidity(page, value):
    hum_slider = page.locator('input[type="range"]').nth(1)
    hum_slider.fill(str(value))



def test_temperature_normal_green_led_log(wokwi_page):
    page = wokwi_page
    page.locator("button[aria-label='Start the simulation']").click()
    print("GET CONSOLE OUTPUT")
    serial_output = read_monitor(page)
    click_on_sensor(page)
    set_temperature(page, 25)
    set_humidity(page, 40)
    time.sleep(3)

    assert "TEMP_STATUS : LOW" in serial_output
    assert "LED         : GREEN" in serial_output
    assert "BUZZER      : OFF" in serial_output


def test_temperature_high_red_led(page):

    set_temperature(page, 38)
    set_humidity(page, 40)
    time.sleep(3)

    serial_output = get_serial_text(page)

    assert "TEMP_STATUS : HIGH" in serial_output
    assert "LED         : RED" in serial_output


def test_humidity_high_buzzer_on(page):

    set_temperature(page, 25)
    set_humidity(page, 80)
    time.sleep(3)

    serial_output = get_serial_text(page)

    assert "HUM_STATUS  : HIGH" in serial_output
    assert "BUZZER      : ON" in serial_output


def test_no_duplicate_logs_on_same_status(page):

    set_temperature(page, 25)
    set_humidity(page, 50)
    time.sleep(3)

    first_log = get_serial_text(page)

    time.sleep(3)
    second_log = get_serial_text(page)

    assert first_log == second_log




def open_dht22_editor(page: Page):
    dht = page.locator("#dht1")
    dht.wait_for(state="visible", timeout=10000)
    dht.click(force=True)

    # Wait until editor panel appears
    page.wait_for_selector('text=Editing DHT22', timeout=5000)


def get_slider_values(page: Page):
    temp_slider = page.locator('input[type="range"]').nth(0)
    hum_slider = page.locator('input[type="range"]').nth(1)

    return {
        "temperature": float(temp_slider.input_value()),
        "humidity": float(hum_slider.input_value()),
    }


def get_dom_values(page: Page):
    return page.evaluate(
        """() => {
            const dht = document.querySelector('#dht1');
            return {
                temperature: parseFloat(dht.getAttribute('temperature')),
                humidity: parseFloat(dht.getAttribute('humidity')),
            };
        }"""
    )


def test_increase_and_decrease_temperature_and_humidity(wokwi_page):
    page = wokwi_page
    page.locator("button[aria-label='Start the simulation']").click()
    print("GET CONSOLE OUTPUT")
    serial_output = read_monitor(page)
    open_dht22_editor(page)

    before_slider = get_slider_values(page)
    before_dom = get_dom_values(page)

    # Increase temperature & humidity
    page.locator('input[type="range"]').nth(0).fill("30")
    page.locator('input[type="range"]').nth(1).fill("60")
    time.sleep(2)

    after_increase_slider = get_slider_values(page)
    after_increase_dom = get_dom_values(page)

    assert after_increase_slider["temperature"] > before_slider["temperature"]
    assert after_increase_slider["humidity"] > before_slider["humidity"]

    assert after_increase_dom["temperature"] == after_increase_slider["temperature"]
    assert after_increase_dom["humidity"] == after_increase_slider["humidity"]

    # Decrease temperature & humidity
    page.locator('input[type="range"]').nth(0).fill("15")
    page.locator('input[type="range"]').nth(1).fill("25")
    time.sleep(2)

    after_decrease_slider = get_slider_values(page)
    after_decrease_dom = get_dom_values(page)

    assert after_decrease_slider["temperature"] < after_increase_slider["temperature"]
    assert after_decrease_slider["humidity"] < after_increase_slider["humidity"]

    assert after_decrease_dom["temperature"] == after_decrease_slider["temperature"]
    assert after_decrease_dom["humidity"] == after_decrease_slider["humidity"]
    serial_output = read_monitor(page)


def get_serial_output(page: Page) -> str:
    return page.locator("textarea").input_value()


def test_slider_change_reflected_in_serial(wokwi_page):
    page = wokwi_page
    page.locator("button[aria-label='Start the simulation']").click()
    print("GET CONSOLE OUTPUT")
    serial_output = read_monitor(page)
    open_dht22_editor(page)

    page.locator('input[type="range"]').nth(0).fill("35")
    page.locator('input[type="range"]').nth(1).fill("80")
    time.sleep(3)

    serial = read_monitor(page)

    assert "TEMP_STATUS : HIGH" in serial
    assert "HUM_STATUS  : HIGH" in serial
    assert "BUZZER      : ON" in serial

def test_temp_low_hum_low(wokwi_page):
    page = wokwi_page
    page.locator("button[aria-label='Start the simulation']").click()
    open_dht22_editor(page)

    page.locator('input[type="range"]').nth(0).fill("15")
    page.locator('input[type="range"]').nth(1).fill("20")
    time.sleep(3)

    serial = read_monitor(page)

    assert "TEMP_STATUS : LOW" in serial
    assert "LED         : YELLOW" in serial
    assert "HUM_STATUS  : LOW" in serial
    assert "BUZZER      : OFF" in serial

def test_temp_normal_hum_low(wokwi_page):
    page = wokwi_page
    page.locator("button[aria-label='Start the simulation']").click()
    open_dht22_editor(page)

    page.locator('input[type="range"]').nth(0).fill("25")
    page.locator('input[type="range"]').nth(1).fill("25")
    time.sleep(3)

    serial = read_monitor(page)

    assert "TEMP_STATUS : NORMAL" in serial
    assert "LED         : GREEN" in serial
    assert "HUM_STATUS  : LOW" in serial
    assert "BUZZER      : OFF" in serial

def test_temp_high_hum_low(wokwi_page):
    page = wokwi_page
    page.locator("button[aria-label='Start the simulation']").click()
    open_dht22_editor(page)

    page.locator('input[type="range"]').nth(0).fill("35")
    page.locator('input[type="range"]').nth(1).fill("20")
    time.sleep(3)

    serial = read_monitor(page)

    assert "TEMP_STATUS : HIGH" in serial
    assert "LED         : RED" in serial
    assert "HUM_STATUS  : LOW" in serial
    assert "BUZZER      : OFF" in serial


def test_temp_low_hum_normal(wokwi_page):
    page = wokwi_page
    page.locator("button[aria-label='Start the simulation']").click()
    open_dht22_editor(page)

    page.locator('input[type="range"]').nth(0).fill("18")
    page.locator('input[type="range"]').nth(1).fill("45")
    time.sleep(3)

    serial = read_monitor(page)

    assert "TEMP_STATUS : LOW" in serial
    assert "LED         : YELLOW" in serial
    assert "HUM_STATUS  : NORMAL" in serial
    assert "BUZZER      : OFF" in serial


def test_temp_normal_hum_normal(wokwi_page):
    page = wokwi_page
    page.locator("button[aria-label='Start the simulation']").click()
    open_dht22_editor(page)

    page.locator('input[type="range"]').nth(0).fill("22")
    page.locator('input[type="range"]').nth(1).fill("50")
    time.sleep(3)

    serial = read_monitor(page)

    assert "TEMP_STATUS : NORMAL" in serial
    assert "LED         : GREEN" in serial
    assert "HUM_STATUS  : NORMAL" in serial
    assert "BUZZER      : OFF" in serial


def test_temp_high_hum_normal(wokwi_page):
    page = wokwi_page
    page.locator("button[aria-label='Start the simulation']").click()
    open_dht22_editor(page)

    page.locator('input[type="range"]').nth(0).fill("32")
    page.locator('input[type="range"]').nth(1).fill("55")
    time.sleep(3)

    serial = read_monitor(page)

    assert "TEMP_STATUS : HIGH" in serial
    assert "LED         : RED" in serial
    assert "HUM_STATUS  : NORMAL" in serial
    assert "BUZZER      : OFF" in serial


def test_temp_low_hum_high(wokwi_page):
    page = wokwi_page
    page.locator("button[aria-label='Start the simulation']").click()
    open_dht22_editor(page)

    page.locator('input[type="range"]').nth(0).fill("15")
    page.locator('input[type="range"]').nth(1).fill("75")
    time.sleep(3)

    serial = read_monitor(page)

    assert "TEMP_STATUS : LOW" in serial
    assert "LED         : YELLOW" in serial
    assert "HUM_STATUS  : HIGH" in serial
    assert "BUZZER      : ON" in serial


def test_temp_high_hum_high(wokwi_page):
    page = wokwi_page
    page.locator("button[aria-label='Start the simulation']").click()
    open_dht22_editor(page)

    page.locator('input[type="range"]').nth(0).fill("38")
    page.locator('input[type="range"]').nth(1).fill("85")
    time.sleep(3)

    serial = read_monitor(page)

    assert "TEMP_STATUS : HIGH" in serial
    assert "LED         : RED" in serial
    assert "HUM_STATUS  : HIGH" in serial
    assert "BUZZER      : ON" in serial


def test_boundary_values_normal(wokwi_page):
    page = wokwi_page
    page.locator("button[aria-label='Start the simulation']").click()
    open_dht22_editor(page)

    page.locator('input[type="range"]').nth(0).fill("20")
    page.locator('input[type="range"]').nth(1).fill("30")
    time.sleep(3)

    serial = read_monitor(page)

    assert "TEMP_STATUS : NORMAL" in serial
    assert "LED         : GREEN" in serial
    assert "HUM_STATUS  : NORMAL" in serial
    assert "BUZZER      : OFF" in serial




