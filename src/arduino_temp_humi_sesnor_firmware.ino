#include <DHT.h>
#include <Adafruit_Sensor.h>

#define DHTPIN 2
#define DHTTYPE DHT22

#define GREEN_LED 8
#define YELLOW_LED 9
#define RED_LED 10
#define BUZZER 11

DHT dht(DHTPIN, DHTTYPE);

String lastTempStatus = "";
String lastHumStatus  = "";

void setup() {
  Serial.begin(9600);
  dht.begin();

  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  digitalWrite(BUZZER, LOW);

  Serial.println("SYSTEM_STARTED");
}

String getTempStatus(float temp) {
  if (temp < 20) return "LOW";
  if (temp <= 30) return "NORMAL";
  return "HIGH";
}

String getHumStatus(float hum) {
  if (hum < 30) return "LOW";
  if (hum <= 60) return "NORMAL";
  return "HIGH";
}

String getLedColor(String tempStatus) {
  if (tempStatus == "LOW") return "YELLOW";
  if (tempStatus == "NORMAL") return "GREEN";
  return "RED";
}

void updateOutputs(String tempStatus, String humStatus) {
  // Reset outputs
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(RED_LED, LOW);
  digitalWrite(BUZZER, LOW);

  // LED logic
  if (tempStatus == "LOW") digitalWrite(YELLOW_LED, HIGH);
  else if (tempStatus == "NORMAL") digitalWrite(GREEN_LED, HIGH);
  else digitalWrite(RED_LED, HIGH);

  // Buzzer logic
  if (humStatus == "HIGH") digitalWrite(BUZZER, HIGH);
}

void printFormattedLog(float temp, float hum,
                       String tempStatus, String humStatus) {

  Serial.println("==============================");
  Serial.println("SYSTEM EVENT");
  Serial.println("==============================");

  Serial.print("TEMP        : ");
  Serial.print(temp);
  Serial.println(" C");

  Serial.print("HUMIDITY    : ");
  Serial.print(hum);
  Serial.println(" %");

  Serial.println("------------------------------");

  Serial.print("TEMP_STATUS : ");
  Serial.println(tempStatus);

  Serial.print("LED         : ");
  Serial.println(getLedColor(tempStatus));

  Serial.print("HUM_STATUS  : ");
  Serial.println(humStatus);

  Serial.print("BUZZER      : ");
  Serial.println(humStatus == "HIGH" ? "ON" : "OFF");

  Serial.println("==============================");
}

void loop() {
  delay(2000);

  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) return;

  String tempStatus = getTempStatus(temp);
  String humStatus  = getHumStatus(hum);

  // Print only on change
  if (tempStatus != lastTempStatus || humStatus != lastHumStatus) {
    updateOutputs(tempStatus, humStatus);
    printFormattedLog(temp, hum, tempStatus, humStatus);

    lastTempStatus = tempStatus;
    lastHumStatus  = humStatus;
  }
}
