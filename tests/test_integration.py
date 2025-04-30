import unittest
from app import app, db
from models import SensorData, FarmerInput, SystemStatus
import json
import paho.mqtt.client as mqtt
import time

class TestIntegration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_complete_flow(self):
        # 1. Simulate MQTT message
        test_payload = {
            'temperature': 25.5,
            'humidity': 60.0,
            'moisture': 500,
            'ph': 6.5
        }

        # 2. Verify sensor data is saved
        with app.app_context():
            sensor_data = SensorData(**test_payload)
            db.session.add(sensor_data)
            db.session.commit()

            # 3. Test GET /api/sensor-data
            response = self.client.get('/api/sensor-data')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['temperature'], 25.5)

            # 4. Test farmer input and prediction
            farmer_input = {
                'soil_type': 'clay',
                'weather': 'sunny',
                'region': 'north'
            }
            response = self.client.post('/api/predict',
                                      data=json.dumps(farmer_input),
                                      content_type='application/json')
            self.assertEqual(response.status_code, 200)
            prediction = json.loads(response.data)
            self.assertIn('crop', prediction)
            self.assertIn('confidence', prediction)

            # 5. Verify prediction is saved
            saved_prediction = FarmerInput.query.first()
            self.assertIsNotNone(saved_prediction)
            self.assertEqual(saved_prediction.soil_type, 'clay')

            # 6. Test system status
            response = self.client.get('/api/system-status')
            self.assertEqual(response.status_code, 200)
            status = json.loads(response.data)
            self.assertIn('status', status)
            self.assertIn('sensor_status', status)

    def test_error_handling(self):
        # Test invalid sensor data
        with app.app_context():
            invalid_data = {
                'temperature': 'invalid',
                'humidity': 60.0,
                'moisture': 500,
                'ph': 6.5
            }
            response = self.client.post('/api/sensor-data',
                                      data=json.dumps(invalid_data),
                                      content_type='application/json')
            self.assertEqual(response.status_code, 400)

        # Test invalid farmer input
        invalid_input = {
            'soil_type': 'invalid_type',
            'weather': 'sunny',
            'region': 'north'
        }
        response = self.client.post('/api/predict',
                                  data=json.dumps(invalid_input),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main() 