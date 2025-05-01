import paho.mqtt.client as mqtt
import requests
import json
import logging
import sys
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuration
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "crop/recommendation"  # Change this to your desired topic
API_ENDPOINT = "http://127.0.0.1:5000/predict"
KEEP_ALIVE = 60

def on_connect(client: mqtt.Client, userdata: Any, flags: Dict, rc: int) -> None:
    """Callback when connected to MQTT broker"""
    if rc == 0:
        logger.info("Successfully connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        logger.error(f"Failed to connect to MQTT broker with code: {rc}")

def on_disconnect(client: mqtt.Client, userdata: Any, rc: int) -> None:
    """Callback when disconnected from MQTT broker"""
    logger.warning(f"Disconnected from MQTT broker with code: {rc}")
    if rc != 0:
        logger.info("Attempting to reconnect...")
        client.reconnect()

def on_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
    """Callback when message is received"""
    try:
        payload = json.loads(msg.payload.decode())
        logger.info(f"Received message on topic {msg.topic}: {payload}")
        
        response = requests.post(API_ENDPOINT, json=payload, timeout=10)
        response.raise_for_status()
        
        prediction = response.json()
        logger.info(f"Prediction result: {prediction}")
        
    except json.JSONDecodeError:
        logger.error("Failed to decode message payload as JSON")
    except requests.RequestException as e:
        logger.error(f"HTTP request failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

def main():
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        
        # Enable automatic reconnection
        client.enable_logger(logger)
        client.reconnect_delay_set(min_delay=1, max_delay=60)
        
        logger.info(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
        client.connect(MQTT_BROKER, MQTT_PORT, KEEP_ALIVE)
        
        # Start the loop
        client.loop_forever()
        
    except KeyboardInterrupt:
        logger.info("Shutting down MQTT client...")
        client.disconnect()
        client.loop_stop()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
