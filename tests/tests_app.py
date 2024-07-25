import unittest
from app import app, db, SensorReading
from datetime import datetime
import io

class SensorDataTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Set up the test database
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_receive_sensor_data(self):
        response = self.app.post('/sensor_data', json={
            "equipmentId": "EQ-12495",
            "timestamp": "2023-02-15T01:30:00.000-05:00",
            "value": 78.42
        })
        self.assertEqual(response.status_code, 201)

    def test_upload_csv(self):
        data = {
            'file': (io.BytesIO(b"EQ-12495,2023-02-15T01:30:00.000-05:00,78.42\n"), 'test.csv')
        }
        response = self.app.post('/upload_csv', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
