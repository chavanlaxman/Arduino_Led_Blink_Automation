int led = 13;
int btn = 7;

static int led_state = 0;
static int prev_btn_data = HIGH;

void setup() {
  Serial.begin(115200);
  pinMode(led, OUTPUT);
  pinMode(btn, INPUT_PULLUP);

  Serial.println("System Started");
}

void loop() {
  int btn_data = digitalRead(btn);

  if (btn_data == LOW && prev_btn_data == HIGH) {
    Serial.println("Button Press Detected");
    delay(50); // debounce

    if (digitalRead(btn) == LOW) {
      led_state = !led_state;
      digitalWrite(led, led_state);

      Serial.print("LED State Changed → ");
      Serial.println(led_state ? "ON" : "OFF");
    }
  }

  prev_btn_data = btn_data;

  // CLEAR SERIAL MONITOR (ANSI Escape)
  Serial.write(27);
  Serial.print("[2J");
  Serial.print("\033[H");

  delay(200);  // optional
}
