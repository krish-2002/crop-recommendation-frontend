import paho.mqtt.client as mqtt
import requests
import json

def on_connect(client, userdata, flags, rc):
    print("MQTT Connected with code:", rc)
    client.subscribe("your/topic")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    print("Received:", payload)
    response = requests.post("http://127.0.0.1:5000/predict", json=payload)
    print("Prediction:", response.json())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()
