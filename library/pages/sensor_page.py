"""
Temperature & Humidity Sensor Page Object
Contains all locators and methods related to sensor simulation
"""
from library.pages.base_page import BasePage
import time


class SensorPage(BasePage):
    """Page object for Temperature & Humidity Sensor simulation"""

    # Locators
    START_SIMULATION_BUTTON = "button[aria-label='Start the simulation']"
    CONSOLE_OUTPUT = ".notranslate"
    DHT_SENSOR_ELEMENT = "#dht1"
    TEMPERATURE_SLIDER = 'input[type="range"]'  # First occurrence
    HUMIDITY_SLIDER = 'input[type="range"]'  # Second occurrence
    SERIAL_TEXTAREA = "textarea"
    EDIT_PANEL_TITLE = 'text=Editing DHT22'

    def start_simulation(self):
        """Start the simulation"""
        print("Starting simulation")
        self.click_element(self.START_SIMULATION_BUTTON)
        self.wait_and_sleep(2)

    def get_console_output(self) -> str:
        """Get console/serial monitor output"""
        print("Reading console output")
        self.wait_and_sleep(10)
        text = self.get_text_from_locator(self.CONSOLE_OUTPUT)
        print(text)
        return text



    def open_dht22_editor(self):
        """Open DHT22 sensor editor panel"""
        print("Opening DHT22 sensor editor")
        dht = self.page.locator(self.DHT_SENSOR_ELEMENT)
        dht.wait_for(state="visible", timeout=10000)
        dht.click(force=True)
        
        # Wait until editor panel appears
        self.page.wait_for_selector(self.EDIT_PANEL_TITLE, timeout=5000)
        print("✓ DHT22 editor panel opened")

    def set_temperature(self, value: float):
        """Set temperature value using slider"""
        print(f"Setting temperature to {value}°C")
        temp_slider = self.page.locator(self.TEMPERATURE_SLIDER).nth(0)
        temp_slider.fill(str(value))
        self.wait_and_sleep(1)

    def set_humidity(self, value: float):
        """Set humidity value using slider"""
        print(f"Setting humidity to {value}%")
        hum_slider = self.page.locator(self.HUMIDITY_SLIDER).nth(1)
        hum_slider.fill(str(value))
        self.wait_and_sleep(1)

    def set_temperature_and_humidity(self, temp: float, humidity: float):
        """Set both temperature and humidity values"""
        self.set_temperature(temp)
        self.set_humidity(humidity)

    def get_slider_values(self) -> dict:
        """Get current values from sliders"""
        temp_slider = self.page.locator(self.TEMPERATURE_SLIDER).nth(0)
        hum_slider = self.page.locator(self.HUMIDITY_SLIDER).nth(1)

        return {
            "temperature": float(temp_slider.input_value()),
            "humidity": float(hum_slider.input_value()),
        }

    def get_dom_values(self) -> dict:
        """Get DHT22 sensor values from DOM"""
        return self.evaluate_js(
            """() => {
                const dht = document.querySelector('#dht1');
                return {
                    temperature: parseFloat(dht.getAttribute('temperature')),
                    humidity: parseFloat(dht.getAttribute('humidity')),
                };
            }"""
        )

    def verify_sensor_values_match(self) -> bool:
        """Verify that slider values match DOM values"""
        slider_values = self.get_slider_values()
        dom_values = self.get_dom_values()

        matches = (
            slider_values["temperature"] == dom_values["temperature"] and
            slider_values["humidity"] == dom_values["humidity"]
        )

        if matches:
            print("✓ Slider values match DOM values")
        else:
            print("✗ Slider values do not match DOM values")

        return matches

    def click_sensor(self):
        """Click on the sensor element"""
        print("Clicking on sensor")
        self.click_element(self.DHT_SENSOR_ELEMENT, force=True)
        self.wait_and_sleep(2)

    def take_sensor_screenshot(self, filename: str = "sensor_screenshot.png"):
        """Take screenshot of current sensor state"""
        self.take_screenshot(filename)
