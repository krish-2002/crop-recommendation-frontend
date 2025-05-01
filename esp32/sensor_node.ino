#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// MQTT Broker settings
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "sensor/data";

// Sensor pins
#define DHT_PIN 4
#define MOISTURE_PIN 34
#define PH_PIN 35

// Sensor types
#define DHT_TYPE DHT11

// Initialize sensors
DHT dht(DHT_PIN, DHT_TYPE);

// Initialize WiFi and MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);

// Timing variables
unsigned long lastMsg = 0;
const long interval = 30000; // 30 seconds

// Calibration values for pH sensor
const float PH_OFFSET = 0.0; // Adjust this based on your sensor calibration
const float PH_SLOPE = 1.0;  // Adjust this based on your sensor calibration

void setup_wifi() {
  delay(10);
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
}

float readPH() {
  int rawValue = analogRead(PH_PIN);
  float voltage = (rawValue * 3.3) / 4095.0; // Convert to voltage (ESP32 has 12-bit ADC)
  float ph = (voltage * PH_SLOPE) + PH_OFFSET;
  return ph;
}

void setup() {
  Serial.begin(115200);
  
  // Initialize sensors
  dht.begin();
  pinMode(MOISTURE_PIN, INPUT);
  pinMode(PH_PIN, INPUT);
  
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > interval) {
    lastMsg = now;
    
    // Read sensor data
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int moisture = analogRead(MOISTURE_PIN);
    float ph = readPH();
    
    // Check if any reads failed
    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
    
    // Create JSON document
    StaticJsonDocument<200> doc;
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["moisture"] = moisture;
    doc["ph"] = ph;
    doc["timestamp"] = now;
    
    // Serialize JSON to string
    String jsonString;
    serializeJson(doc, jsonString);
    
    // Publish to MQTT
    if (client.publish(mqtt_topic, jsonString.c_str())) {
      Serial.println("Message published successfully");
      Serial.println(jsonString);
    } else {
      Serial.println("Message publish failed");
    }
  }
} 