import unittest
from flask import Flask
from app import app

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_login_incorrect_credentials(self):
        response = self.app.post('/login', data={
            'email': 'Ride@Johnny.com',
            'password': 'Heaven'  # Use incorrect password
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login Failed', response.data)  # Add assertion for failure message or relevant content

if __name__ == '__main__':
    unittest.main()
