import pytest
from library.pages import SensorPage


@pytest.fixture
def sensor_page(wokwi_page):
    """Create Sensor page object instance"""
    return SensorPage(wokwi_page)


@pytest.mark.sensor
def test_system_startup(sensor_page):
    """Verify Arduino system startup"""
    print("Starting simulation")
    sensor_page.start_simulation()
    text = sensor_page.get_console_output()
    assert 'SYSTEM_STARTED' in text, "Arduino simulator not started"


@pytest.mark.sensor
def test_temperature_normal_green_led_log(sensor_page):
    """Test normal temperature results in green LED"""
    sensor_page.start_simulation()
    sensor_page.click_sensor()
    sensor_page.set_temperature_and_humidity(25, 40)
    sensor_page.wait_and_sleep(3)

    serial_output = sensor_page.get_console_output()

    assert "TEMP_STATUS : LOW" in serial_output or "TEMP_STATUS : NORMAL" in serial_output
    assert "LED         : GREEN" in serial_output or "LED         : YELLOW" in serial_output
    assert "BUZZER      : OFF" in serial_output


@pytest.mark.sensor
def test_temperature_high_red_led(sensor_page):
    """Test high temperature results in red LED"""
    sensor_page.start_simulation()
    sensor_page.click_sensor()
    sensor_page.set_temperature(38)
    sensor_page.set_humidity(40)
    sensor_page.wait_and_sleep(3)

    serial_output = sensor_page.get_console_output()

    assert "TEMP_STATUS : HIGH" in serial_output
    assert "LED         : RED" in serial_output


@pytest.mark.sensor
def test_humidity_high_buzzer_on(sensor_page):
    """Test high humidity turns on buzzer"""
    sensor_page.start_simulation()
    sensor_page.get_console_output()
    sensor_page.open_dht22_editor()
    sensor_page.set_temperature(25)
    sensor_page.set_humidity(80)
    sensor_page.wait_and_sleep(3)

    serial_output = sensor_page.get_console_output()

    assert "HUM_STATUS  : HIGH" in serial_output
    assert "BUZZER      : ON" in serial_output


@pytest.mark.skip
def test_no_duplicate_logs_on_same_status(sensor_page):
    """Test no duplicate logs when status doesn't change"""
    sensor_page.start_simulation()
    sensor_page.get_console_output()
    sensor_page.open_dht22_editor()
    sensor_page.set_temperature(25)
    sensor_page.set_humidity(50)
    sensor_page.wait_and_sleep(3)

    first_log = sensor_page.get_console_output()

    sensor_page.wait_and_sleep(3)
    second_log = sensor_page.get_console_output()

    assert first_log == second_log, "Duplicate logs detected"


@pytest.mark.sensor
def test_increase_and_decrease_temperature_and_humidity(sensor_page):
    """Test increasing and decreasing temperature and humidity values"""
    sensor_page.start_simulation()
    sensor_page.get_console_output()
    sensor_page.open_dht22_editor()

    before_slider = sensor_page.get_slider_values()
    before_dom = sensor_page.get_dom_values()

    # Increase temperature & humidity
    sensor_page.set_temperature_and_humidity(30, 60)
    sensor_page.wait_and_sleep(2)

    after_increase_slider = sensor_page.get_slider_values()
    after_increase_dom = sensor_page.get_dom_values()

    assert after_increase_slider["temperature"] > before_slider["temperature"], \
        "Temperature increase failed"
    assert after_increase_slider["humidity"] > before_slider["humidity"], \
        "Humidity increase failed"

    assert after_increase_dom["temperature"] == after_increase_slider["temperature"], \
        "DOM temperature doesn't match slider"
    assert after_increase_dom["humidity"] == after_increase_slider["humidity"], \
        "DOM humidity doesn't match slider"

    # Decrease temperature & humidity
    sensor_page.set_temperature_and_humidity(15, 25)
    sensor_page.wait_and_sleep(2)

    after_decrease_slider = sensor_page.get_slider_values()
    after_decrease_dom = sensor_page.get_dom_values()

    assert after_decrease_slider["temperature"] < after_increase_slider["temperature"], \
        "Temperature decrease failed"
    assert after_decrease_slider["humidity"] < after_increase_slider["humidity"], \
        "Humidity decrease failed"

    assert after_decrease_dom["temperature"] == after_decrease_slider["temperature"], \
        "DOM temperature doesn't match after decrease"
    assert after_decrease_dom["humidity"] == after_decrease_slider["humidity"], \
        "DOM humidity doesn't match after decrease"


@pytest.mark.sensor
def test_slider_change_reflected_in_serial(sensor_page):
    """Test slider changes are reflected in serial output"""
    sensor_page.start_simulation()
    sensor_page.get_console_output()
    sensor_page.open_dht22_editor()

    sensor_page.set_temperature_and_humidity(35, 80)
    sensor_page.wait_and_sleep(3)

    serial = sensor_page.get_console_output()

    assert "TEMP_STATUS : HIGH" in serial
    assert "HUM_STATUS  : HIGH" in serial
    assert "BUZZER      : ON" in serial


@pytest.mark.sensor
def test_temp_low_hum_low(sensor_page):
    """Test low temperature and low humidity combination"""
    sensor_page.start_simulation()
    sensor_page.open_dht22_editor()

    sensor_page.set_temperature_and_humidity(15, 20)
    sensor_page.wait_and_sleep(3)

    serial = sensor_page.get_console_output()

    assert "TEMP_STATUS : LOW" in serial
    assert "LED         : YELLOW" in serial
    assert "HUM_STATUS  : LOW" in serial
    assert "BUZZER      : OFF" in serial


@pytest.mark.sensor
def test_temp_normal_hum_low(sensor_page):
    """Test normal temperature and low humidity combination"""
    sensor_page.start_simulation()
    sensor_page.open_dht22_editor()

    sensor_page.set_temperature_and_humidity(25, 25)
    sensor_page.wait_and_sleep(3)

    serial = sensor_page.get_console_output()

    assert "TEMP_STATUS : NORMAL" in serial
    assert "LED         : GREEN" in serial
    assert "HUM_STATUS  : LOW" in serial
    assert "BUZZER      : OFF" in serial


@pytest.mark.sensor
def test_temp_high_hum_low(sensor_page):
    """Test high temperature and low humidity combination"""
    sensor_page.start_simulation()
    sensor_page.open_dht22_editor()

    sensor_page.set_temperature_and_humidity(35, 20)
    sensor_page.wait_and_sleep(3)

    serial = sensor_page.get_console_output()

    assert "TEMP_STATUS : HIGH" in serial
    assert "LED         : RED" in serial
    assert "HUM_STATUS  : LOW" in serial
    assert "BUZZER      : OFF" in serial


@pytest.mark.sensor
def test_temp_low_hum_normal(sensor_page):
    """Test low temperature and normal humidity combination"""
    sensor_page.start_simulation()
    sensor_page.open_dht22_editor()

    sensor_page.set_temperature_and_humidity(18, 45)
    sensor_page.wait_and_sleep(3)

    serial = sensor_page.get_console_output()

    assert "TEMP_STATUS : LOW" in serial
    assert "LED         : YELLOW" in serial
    assert "HUM_STATUS  : NORMAL" in serial
    assert "BUZZER      : OFF" in serial


@pytest.mark.sensor
def test_temp_normal_hum_normal(sensor_page):
    """Test normal temperature and normal humidity combination"""
    sensor_page.start_simulation()
    sensor_page.open_dht22_editor()

    sensor_page.set_temperature_and_humidity(22, 50)
    sensor_page.wait_and_sleep(3)

    serial = sensor_page.get_console_output()

    assert "TEMP_STATUS : NORMAL" in serial
    assert "LED         : GREEN" in serial
    assert "HUM_STATUS  : NORMAL" in serial
    assert "BUZZER      : OFF" in serial


@pytest.mark.sensor
def test_temp_high_hum_normal(sensor_page):
    """Test high temperature and normal humidity combination"""
    sensor_page.start_simulation()
    sensor_page.open_dht22_editor()

    sensor_page.set_temperature_and_humidity(32, 55)
    sensor_page.wait_and_sleep(3)

    serial = sensor_page.get_console_output()

    assert "TEMP_STATUS : HIGH" in serial
    assert "LED         : RED" in serial
    assert "HUM_STATUS  : NORMAL" in serial
    assert "BUZZER      : OFF" in serial


@pytest.mark.sensor
def test_temp_low_hum_high(sensor_page):
    """Test low temperature and high humidity combination"""
    sensor_page.start_simulation()
    sensor_page.open_dht22_editor()

    sensor_page.set_temperature_and_humidity(15, 75)
    sensor_page.wait_and_sleep(3)

    serial = sensor_page.get_console_output()

    assert "TEMP_STATUS : LOW" in serial
    assert "LED         : YELLOW" in serial
    assert "HUM_STATUS  : HIGH" in serial
    assert "BUZZER      : ON" in serial


@pytest.mark.sensor
def test_temp_high_hum_high(sensor_page):
    """Test high temperature and high humidity combination"""
    sensor_page.start_simulation()
    sensor_page.open_dht22_editor()

    sensor_page.set_temperature_and_humidity(38, 85)
    sensor_page.wait_and_sleep(3)

    serial = sensor_page.get_console_output()

    assert "TEMP_STATUS : HIGH" in serial
    assert "LED         : RED" in serial
    assert "HUM_STATUS  : HIGH" in serial
    assert "BUZZER      : ON" in serial


@pytest.mark.sensor
def test_boundary_values_normal(sensor_page):
    """Test boundary values for normal temperature and humidity"""
    sensor_page.start_simulation()
    sensor_page.open_dht22_editor()

    sensor_page.set_temperature_and_humidity(20, 30)
    sensor_page.wait_and_sleep(3)

    serial = sensor_page.get_console_output()

    assert "TEMP_STATUS : NORMAL" in serial or "TEMP_STATUS : LOW" in serial
    assert "LED         : GREEN" in serial or "LED         : YELLOW" in serial
    assert "HUM_STATUS  : NORMAL" in serial or "HUM_STATUS  : LOW" in serial
    assert "BUZZER      : OFF" in serial




