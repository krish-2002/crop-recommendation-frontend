from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import paho.mqtt.client as mqtt
from models import db, SensorData, FarmerInput, SystemStatus
import os
from dotenv import load_dotenv
import time
from ml_model import CropRecommendationModel
import logging
import sys

print("Starting application...")

# Load environment variables
load_dotenv()
print("Environment variables loaded")

app = Flask(__name__)
CORS(app)
print("Flask app created with CORS enabled")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
print("Logging configured")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crop_recommendation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
print("Database initialized")

# MQTT Configuration
MQTT_BROKER = os.getenv('MQTT_BROKER', 'd910d8c7f2cb4f40abeeded6baf814e7.s1.eu.hivemq.cloud')
MQTT_PORT = int(os.getenv('MQTT_PORT', '8883'))
MQTT_USER = os.getenv('MQTT_USER', 'FY2025')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', 'Krish@2025')
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'sensor/data')
MQTT_KEEPALIVE = int(os.getenv('MQTT_KEEPALIVE', '60'))
MQTT_RECONNECT_DELAY = 5  # seconds
print("MQTT configuration loaded")

# Initialize MQTT client
mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)
print("MQTT client initialized")

# Initialize ML model with dataset
dataset_path = os.path.join('data', 'crop_recommendation.csv')
try:
    model = CropRecommendationModel()
    print("ML model initialized")
except Exception as e:
    print(f"Error initializing ML model: {e}")
    sys.exit(1)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT broker successfully")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"❌ Failed to connect to MQTT broker with code: {rc}")
        print("Error codes:")
        print("0: Connection successful")
        print("1: Connection refused - incorrect protocol version")
        print("2: Connection refused - invalid client identifier")
        print("3: Connection refused - server unavailable")
        print("4: Connection refused - bad username or password")
        print("5: Connection refused - not authorized")
        # Attempt to reconnect after delay
        time.sleep(MQTT_RECONNECT_DELAY)
        client.reconnect()

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"❌ Unexpected disconnection from MQTT broker with code: {rc}")
        print("Attempting to reconnect...")
        time.sleep(MQTT_RECONNECT_DELAY)
        client.reconnect()

def on_message(client, userdata, msg):
    with app.app_context():
        try:
            payload = json.loads(msg.payload.decode())
            # Validate payload
            required_fields = ['temperature', 'humidity', 'moisture', 'ph']
            if not all(field in payload for field in required_fields):
                print("❌ Invalid payload: missing required fields")
                return

            # Create new sensor data entry
            sensor_data = SensorData(
                temperature=payload['temperature'],
                humidity=payload['humidity'],
                moisture=payload['moisture'],
                ph=payload['ph']
            )
            db.session.add(sensor_data)
            db.session.commit()
            print("✅ Sensor data saved to database")
        except json.JSONDecodeError:
            print("❌ Error decoding JSON payload")
        except Exception as e:
            print(f"❌ Error processing MQTT message: {e}")

def connect_mqtt():
    try:
        # Set up MQTT client with error handling
        mqtt_client.on_connect = on_connect
        mqtt_client.on_disconnect = on_disconnect
        mqtt_client.on_message = on_message
        
        # Set username and password
        mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        
        # Set TLS/SSL
        mqtt_client.tls_set()
        
        # Connect to broker
        print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        
        # Start the loop
        mqtt_client.loop_start()
        
    except Exception as e:
        print(f"❌ Error connecting to MQTT broker: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(MQTT_RECONNECT_DELAY)
        connect_mqtt()

# Initial MQTT connection
connect_mqtt()

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    try:
        logger.info("Fetching sensor data...")
        # Get the last 24 hours of data
        data = SensorData.query.order_by(SensorData.timestamp.desc()).limit(100).all()
        logger.info(f"Found {len(data)} sensor records")
        return jsonify([item.to_dict() for item in data])
    except Exception as e:
        logger.error(f"Error fetching sensor data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        logger.info(f"Received prediction request with data: {data}")
        
        # Validate required fields
        required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 
                         'soil_type', 'weather', 'region']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
            
        # Make prediction
        result = model.predict(data)
        logger.info(f"Prediction result: {result}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/train', methods=['POST'])
def train():
    try:
        data = request.get_json()
        if 'dataset_path' not in data:
            return jsonify({
                'error': 'dataset_path is required'
            }), 400
            
        model.train(data['dataset_path'])
        return jsonify({
            'message': 'Model trained successfully'
        })
        
    except Exception as e:
        logger.error(f"Error in training: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/system-status', methods=['GET'])
def get_system_status():
    try:
        logger.info("Fetching system status...")
        # Get latest sensor data
        latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()
        
        if not latest_data:
            status = "offline"
            message = "No sensor data available"
            logger.warning("System status: offline - No sensor data")
        else:
            # Check if data is recent (within last 5 minutes)
            time_diff = datetime.utcnow() - latest_data.timestamp
            if time_diff.total_seconds() > 300:
                status = "error"
                message = "Sensor data is not recent"
                logger.warning("System status: error - Data not recent")
            else:
                status = "online"
                message = "System is functioning normally"
                logger.info("System status: online")

        # Create system status entry
        system_status = SystemStatus(
            status=status,
            message=message,
            sensor_status={
                'temperature': latest_data.temperature if latest_data else None,
                'humidity': latest_data.humidity if latest_data else None,
                'moisture': latest_data.moisture if latest_data else None,
                'ph': latest_data.ph if latest_data else None
            }
        )
        db.session.add(system_status)
        db.session.commit()
        logger.info("System status saved to database")

        return jsonify(system_status.to_dict())
    except Exception as e:
        logger.error(f"Error fetching system status: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        print("Creating database tables...")
        with app.app_context():
            db.create_all()
        print("Database tables created successfully")
        
        print("Starting Flask server...")
        port = int(os.environ.get('PORT', 5001))
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
