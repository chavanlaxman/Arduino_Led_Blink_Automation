import time

from playwright.sync_api import Page


def open_project(page: Page, url):
    page.goto(url, timeout=120000)
    print(page.title())
    print(f"Succssfully Navigated to {url}")


def stop_simulation(page: Page):
    simulation_stoped = False
    if page.locator("button[aria-label='Stop the simulation']").is_visible():
        simulation_started = True
        return simulation_started
    else:
        print("Simulation stop Button not found")
        page.screenshot("stop_simulation_button_not_found.png")
        return simulation_stoped


def start_simulation(page: Page):
    """
    This methid will verify is simulation started
    :param wokwi_page:
    :return:
    """
    simulation_started = False
    if page.locator("button[aria-label='Restart the simulation']").click():
        print("Successfully click on Run Simulation Button")
        simulation_started = True
        return simulation_started
    else:
        print("Simulation Green Button not found")
        return simulation_started


def pause_simulation(page: Page):
    """
    This methid will verify is simulation started
    :param wokwi_page:
    :return:
    """
    pause_simulation = False
    if page.locator("button[aria-label='Pause']").click():
        print("Successfully click on Pause Simulation Button")
        pause_simulation = True
        return pause_simulation
    else:
        print("Simulation Green Button not found")
        return pause_simulation


def press_push_buttons(page: Page, button_id: str = "btn1", hold_ms: int = 300, led_state=''):
    """
    Physically presses a Wokwi push button by simulating a real pointer press.
    """

    button = page.locator(f"wokwi-pushbutton#{button_id}")
    button.wait_for(state="attached")

    # Get real screen coordinates
    box = button.bounding_box()
    if not box:
        raise Exception("Unable to determine button position")

    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2

    # IMPORTANT: pointer down + delay + pointer up
    for i in range(20):
        print("*" * 68)
        print(f"------------------STARTED ITERATION NO : {i} -------------------------")
        page.mouse.move(x, y)
        page.mouse.down()
        page.wait_for_timeout(hold_ms)
        page.mouse.up()

        print(f"Push button '{button_id}' pressed for {hold_ms} ms")
        text = read_monitor(page)
        try:
            if led_state == "ON":
                assert led_state in text
                print("VERIFIED LED STATE CHANGES FROM OFF ==> ON Successfully")
                break
            elif led_state == "OFF":
                assert led_state in text
                print("VERIFIED LED STATE CHANGE FROM ON ==> OFF Successfully")
                break
            else:
                print("Looping LED ON=>OFF=>ON and vice verse")
        except Exception as e:
            print(f"Expected LED state not found retrying {i}")
            print(f"console output is {text}")

        print("*" * 68)
        print(f"---------------- COMPLETED ITERATION NO : {i} -----------------------")
        print("WAIT 10 SEC FOR NEXT ITERATION ")
        time.sleep(10)


def read_monitor(page: Page):
    ".notranslate"
    print("reading cosole")
    text = page.locator(".notranslate").inner_text()
    print(text)
    return text
