import unittest
from flask import Flask
from app import app

class LogoutTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_logout(self):
        # Simulate login before logout
        login_response = self.app.post('/login', data={
            'email': 'Ride@Johnny.com',
            'password': 'Hell'
        })

        # Ensure login was successful before attempting logout
        self.assertEqual(login_response.status_code, 302)  # Assuming successful login redirects to another page

        # Perform logout
        logout_response = self.app.post('/logout')

        # Assert the expected response
        self.assertEqual(logout_response.status_code, 200)
        self.assertIn(b'Logout successful', logout_response.data)  # Add assertion for success message or relevant content

if __name__ == '__main__':
    unittest.main()
