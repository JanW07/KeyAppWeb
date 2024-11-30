import unittest
from create_main import create_app
import hashlib

class DeviceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Log in to access protected routes
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin'
        })

        # Set up headers for server authorization and a sample device
        self.headers = {
            'Device-ID': 'b7ca6bea7e31aadd6bf2e05f3cb34ef'
        }
        
        # Sample device information
        self.sample_device_info = {
            "info": {
                "device_name": "Test Device",
                "os": "Test OS",
                "version": "1.0"
            }
        }
        
        # Add the device
        response = self.client.post('/authenticate', headers=self.headers, json=self.sample_device_info)
        self.assertIn(response.status_code, [200, 201])  # Accept 200 if device exists, 201 if newly created

    def test_device_listing(self):
        """Test listing all devices"""
        response = self.client.get('/devices', headers=self.headers, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'authorized', response.data)

    def test_authorize_device(self):
        """Test authorizing a device"""
        response = self.client.post(f'/authorize_device/b7ca6bea7e31aadd6bf2e05f3cb34ef', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Device authorized successfully', response.data)

    def test_block_device(self):
        """Test blocking a device"""
        response = self.client.post(f'/block_device/b7ca6bea7e31aadd6bf2e05f3cb34ef', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Device blocked successfully', response.data)

    def test_delete_device(self):
        """Test deleting a device"""
        response = self.client.delete(f'/delete_device/b7ca6bea7e31aadd6bf2e05f3cb34ef', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Device deleted successfully', response.data)

    def test_authenticate_device(self):
        """Test authenticating a new device"""
        response = self.client.post('/authenticate', headers=self.headers, json=self.sample_device_info)
        self.assertIn(response.status_code, [200, 201])  # 200 if exists, 201 if newly created

    def tearDown(self):
        """Clean up by ensuring the test device is deleted if it exists"""
        self.client.delete(f'/delete_device/b7ca6bea7e31aadd6bf2e05f3cb34ef', headers=self.headers)

if __name__ == '__main__':
    unittest.main()
