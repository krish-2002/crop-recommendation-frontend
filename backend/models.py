from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    moisture = db.Column(db.Integer)
    nitrogen = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    potassium = db.Column(db.Float)
    prediction = db.Column(db.String(50))
    confidence = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'temperature': self.temperature,
            'humidity': self.humidity,
            'moisture': self.moisture,
            'nitrogen': self.nitrogen,
            'phosphorus': self.phosphorus,
            'potassium': self.potassium,
            'prediction': self.prediction,
            'confidence': self.confidence
        }

class FarmerInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    soil_type = db.Column(db.String(50))  # e.g., 'clay', 'sandy', 'loamy'
    weather = db.Column(db.String(50))    # e.g., 'sunny', 'rainy', 'cloudy'
    region = db.Column(db.String(100))    # e.g., 'north', 'south', 'east', 'west'
    temperature = db.Column(db.Float)     # Current temperature
    humidity = db.Column(db.Float)        # Current humidity
    moisture = db.Column(db.Integer)      # Current soil moisture
    nitrogen = db.Column(db.Float)        # Nitrogen content
    phosphorus = db.Column(db.Float)      # Phosphorus content
    potassium = db.Column(db.Float)       # Potassium content
    prediction = db.Column(db.String(50)) # Recommended crop
    confidence = db.Column(db.Float)      # Prediction confidence

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'soil_type': self.soil_type,
            'weather': self.weather,
            'region': self.region,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'moisture': self.moisture,
            'nitrogen': self.nitrogen,
            'phosphorus': self.phosphorus,
            'potassium': self.potassium,
            'prediction': self.prediction,
            'confidence': self.confidence
        }

class SystemStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))  # 'online', 'offline', 'error'
    message = db.Column(db.String(200))
    sensor_status = db.Column(db.JSON)

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status,
            'message': self.message,
            'sensor_status': self.sensor_status
        } 