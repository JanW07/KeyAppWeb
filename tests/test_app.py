import unittest
import json
import os
from datetime import timedelta
from create_main import create_app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=2)
        self.client = self.app.test_client()

        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        with open(config_path) as f:
            config = json.load(f)
            self.valid_username = config['username']
            self.valid_password = config['password']

    def test_login_success(self):
        response = self.client.post('/login', data={
            'username': self.valid_username,
            'password': self.valid_password
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Gate Control System', response.data)
        

    def tearDown(self):
        pass

    

if __name__ == '__main__':
    unittest.main()
