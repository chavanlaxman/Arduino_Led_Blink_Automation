import pytest
import time
from library.pages import LEDBlinKPage


@pytest.fixture
def led_page(wokwi_page):
    """Create LED page object instance"""
    return LEDBlinKPage(wokwi_page)


@pytest.mark.led
def test_system_startup(led_page):
    """Verify Arduino system startup"""
    print("Starting simulation")
    led_page.start_simulation()
    text = led_page.get_console_output()
    assert 'SYSTEM_STARTED' in text, "Arduino simulator not started"


@pytest.mark.led
def test_is_simulation_button_present(led_page):
    """Verify if simulation button is present and visible"""
    assert led_page.is_simulation_started(), "Simulation button not found"


@pytest.mark.led
def test_simulation_led_blink_off_to_on(led_page):
    """Test LED blink transition from OFF to ON"""
    led_page.fit_screen()
    led_page.start_simulation()
    assert led_page.press_push_button("btn1", hold_ms=500, led_state="ON"), \
        "LED did not transition to ON state"


@pytest.mark.led
def test_simulation_led_blink_on_to_off(led_page):
    """Test LED blink transition from ON to OFF"""
    led_page.fit_screen()
    led_page.start_simulation()
    assert led_page.press_push_button("btn1", hold_ms=500, led_state="OFF"), \
        "LED did not transition to OFF state"


@pytest.mark.led
def test_simulation_led_blink_loop(led_page):
    """Test LED blink loop behavior"""
    led_page.fit_screen()
    led_page.start_simulation()
    assert led_page.press_push_button("btn1", hold_ms=500), \
        "LED blink loop test failed"

