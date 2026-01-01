"""
LED Blink Project Page Object
Contains all locators and methods related to LED blink simulation
"""
from library.pages.base_page import BasePage
import time


class LEDBlinKPage(BasePage):
    """Page object for LED Blink simulation"""

    # Locators
    START_SIMULATION_BUTTON = "button[aria-label='Start the simulation']"
    RESTART_SIMULATION_BUTTON = "button[aria-label='Restart the simulation']"
    STOP_SIMULATION_BUTTON = "button[aria-label='Stop the simulation']"
    PAUSE_SIMULATION_BUTTON = "button[aria-label='Pause']"
    PUSH_BUTTON = "wokwi-pushbutton#{button_id}"
    CONSOLE_OUTPUT = ".notranslate"

    def start_simulation(self):
        """Start the simulation"""
        print("Clicking START SIMULATION button")
        self.click_element(self.START_SIMULATION_BUTTON)
        self.wait_and_sleep(2)

    def restart_simulation(self):
        """Restart the simulation"""
        print("Clicking RESTART SIMULATION button")
        self.click_element(self.RESTART_SIMULATION_BUTTON)
        self.wait_and_sleep(2)

    def stop_simulation(self):
        """Stop the simulation"""
        print("Clicking STOP SIMULATION button")
        if self.is_element_visible(self.STOP_SIMULATION_BUTTON):
            self.click_element(self.STOP_SIMULATION_BUTTON)
            return True
        else:
            print("Simulation stop button not found")
            return False

    def pause_simulation(self):
        """Pause the simulation"""
        print("Clicking PAUSE button")
        if self.is_element_visible(self.PAUSE_SIMULATION_BUTTON):
            self.click_element(self.PAUSE_SIMULATION_BUTTON)
            return True
        else:
            print("Simulation pause button not found")
            return False

    def is_simulation_started(self) -> bool:
        """Check if simulation can be started"""
        return self.is_element_visible(self.START_SIMULATION_BUTTON)

    def fit_screen(self):
        """Fit the screen for mouse click actions"""
        print("Fitting screen for mouse click action")
        self.press_key("Shift+KeyF")
        self.wait_and_sleep(1)

    def get_console_output(self) -> str:
        """Get console/monitor output"""
        print("Reading console output")
        self.wait_and_sleep(10)
        text = self.get_text_from_locator(self.CONSOLE_OUTPUT)
        print(text)
        return text

    def press_push_button(self, button_id: str = "btn1", hold_ms: int = 300, 
                         led_state: str = '', iterations: int = 20) -> bool:
        """
        Press push button and verify LED state changes
        
        Args:
            button_id: Button element ID
            hold_ms: How long to hold the button in milliseconds
            led_state: Expected LED state ('ON', 'OFF', or empty for looping)
            iterations: Number of iterations to try
            
        Returns:
            True if state verified, False otherwise
        """
        button_locator = self.PUSH_BUTTON.replace("{button_id}", button_id)
        button = self.page.locator(button_locator)
        button.wait_for(state="attached")

        # Get real screen coordinates
        box = button.bounding_box()
        if not box:
            raise Exception("Unable to determine button position")

        x = box["x"] + box["width"] / 2
        y = box["y"] + box["height"] / 2

        for i in range(iterations):
            print("*" * 68)
            print(f"------ ITERATION {i} ------")
            
            self.page.mouse.move(x, y)
            self.page.mouse.down()
            self.page.wait_for_timeout(hold_ms)
            self.page.mouse.up()

            print(f"Push button '{button_id}' pressed for {hold_ms} ms")
            text = self.get_console_output()
            
            try:
                if led_state == "ON":
                    assert "ON" in text
                    print("✓ LED state changed to ON")
                    self.take_screenshot("led_on.png")
                    return True
                elif led_state == "OFF":
                    assert "OFF" in text
                    print("✓ LED state changed to OFF")
                    self.take_screenshot("led_off.png")
                    return True
                else:
                    print("Looping LED ON=>OFF=>ON")
                    return True
            except Exception as e:
                print(f"Expected LED state not found, retrying {i}")
                print(f"Console output: {text}")

            print("*" * 68)
            self.wait_and_sleep(10)

        return False

    def take_led_screenshot(self, filename: str = "led_screenshot.png"):
        """Take screenshot of LED state"""
        self.take_screenshot(filename)
