import unittest
from app import app, db
from models import SensorData, FarmerInput, SystemStatus
import json

class TestApp(unittest.TestCase):
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

    def test_get_sensor_data(self):
        # Create test sensor data
        with app.app_context():
            sensor_data = SensorData(
                temperature=25.5,
                humidity=60.0,
                moisture=500,
                ph=6.5
            )
            db.session.add(sensor_data)
            db.session.commit()

        # Test GET /api/sensor-data
        response = self.client.get('/api/sensor-data')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['temperature'], 25.5)

    def test_predict_crop(self):
        # Create test sensor data
        with app.app_context():
            sensor_data = SensorData(
                temperature=25.5,
                humidity=60.0,
                moisture=500,
                nitrogen=45.0,
                phosphorus=35.0,
                potassium=40.0
            )
            db.session.add(sensor_data)
            db.session.commit()

        # Test POST /api/predict
        test_data = {
            'soil_type': 'clay',
            'weather': 'sunny',
            'region': 'north'
        }
        response = self.client.post('/api/predict',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('crop', data)
        self.assertIn('confidence', data)

    def test_system_status(self):
        # Test GET /api/system-status
        response = self.client.get('/api/system-status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('message', data)
        self.assertIn('sensor_status', data)

if __name__ == '__main__':
    unittest.main() 