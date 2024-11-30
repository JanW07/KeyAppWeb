import unittest
from create_main import create_app

class GateTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Log in to access protected routes
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin'
        })

        # Add the authorization token here
        self.headers = {
            'Authorization': 'my_server_token'
        }

    def test_open_gate(self):
        # Happy path: Attempt to open the gate when it's closed
        response = self.client.post('/open', headers=self.headers, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'open', response.data)

        # Sad path: Attempt to open the gate again when it's already open
        response = self.client.post('/open', headers=self.headers, follow_redirects=True)
        self.assertEqual(response.status_code, 400)  # Assuming a 400 response when already open
        self.assertIn(b'Gate is already open', response.data)

    def test_close_gate(self):
        # First, open the gate to ensure it can be closed
        self.client.post('/open', headers=self.headers, follow_redirects=True)
        
        # Happy path: Attempt to close the gate when it's open
        response = self.client.post('/close', headers=self.headers, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"message":"Gate is closing."', response.data)

        # Sad path: Attempt to close the gate again when it's already closed
        response = self.client.post('/close', headers=self.headers, follow_redirects=True)
        self.assertEqual(response.status_code, 400)  # Assuming a 400 response when already closed
        self.assertIn(b'Gate is already closed', response.data)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
