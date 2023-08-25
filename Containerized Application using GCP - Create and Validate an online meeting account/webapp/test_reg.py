import unittest
from flask import Flask
from app import app

class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_register(self):
        response = self.app.post('/register', data={
            'name': 'Ghost Rider',
            'email': 'Ride@Johnny.com',
            'password': 'Hell',
            'location': 'New York'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful!', response.data)

if __name__ == '__main__':
    unittest.main()
