"""
    Main test
"""
import unittest
import uuid
import json
from api import app
from api.models.user import user

class main_tests(unittest.TestCase):
    """
        Main test
    """
    url_prefix = '/api/v1/'
    def setUp(self):
        """
            Set up tet data
        """
        self.app = app.test_client()
        self.app.testing = True

        self.sample_user = {
            'id': uuid.uuid4().hex,
            'names': 'Muhozi Emery',
            'email': 'emery@andela.com',
            'password': 'secret',
            'confirm_password': 'secret'
        }
        self.exist_user = {
            'names': 'Kudo Kaka',
            'email': 'kaka@andela.com',
            'password': 'secret',
            'confirm_password': 'secret'
        }
        save_user = user();
        save_user.save({
            'names':self.sample_user['names'],
            'email':self.sample_user['email'],
            'password':self.sample_user['password'],
            'confirm_password':self.sample_user['confirm_password']
        })

    def test_registration(self):
        '''
            Testing registration
        '''
        response = self.app.post(self.url_prefix+'auth/register',data = {
            'names':self.exist_user['names'],
            'email':self.exist_user['email'],
            'password':self.exist_user['password'],
            'confirm_password':self.exist_user['confirm_password']
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'have been successfully registered', response.data)

    def test_login(self):
        '''
            Testing login
        '''
        response = self.app.post(self.url_prefix+'auth/login',data = {
            'email':self.sample_user['email'],
            'password':self.sample_user['password']
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'welcome', response.data)

if __name__ == '__main__':
    unittest.main()
