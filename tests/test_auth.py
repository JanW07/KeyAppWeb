import unittest
from datetime import timedelta
from create_main import create_app

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=2)
        self.client = self.app.test_client()

    def test_logout(self):
        # Login first
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin'
        })
        
        # Test logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
