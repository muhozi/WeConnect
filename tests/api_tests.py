"""
    Main test
"""
import unittest
import uuid
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
        save_user = user()
        save_user.save({
            'id': self.sample_user['id'],
            'names': self.sample_user['names'],
            'email': self.sample_user['email'],
            'password': self.sample_user['password'],
            'confirm_password': self.sample_user['confirm_password']
        })

    def test_registration(self):
        '''
            Testing registration
        '''
        # Test registration with complete data
        response = self.app.post(self.url_prefix + 'auth/register', data={
            'names': self.exist_user['names'],
            'email': self.exist_user['email'],
            'password': self.exist_user['password'],
            'confirm_password': self.exist_user['confirm_password']
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'have been successfully registered', response.data)
        # Test registration with incomplete data
        incomplete_data_response = self.app.post(self.url_prefix + 'auth/register', data={
            'names': 'dummy name',
            'confirm_password': self.exist_user['confirm_password']
        })
        self.assertEqual(incomplete_data_response.status_code, 400)
        self.assertIn(b'Please provide', incomplete_data_response.data)

    def test_login(self):
        '''
            Testing login
        '''
        wrong_password_response = self.app.post(self.url_prefix + 'auth/login', data={
            'email': self.sample_user['email'],
            'password': 'anyinvalidpassword'
        })
        self.assertEqual(wrong_password_response.status_code, 401)
        self.assertIn(b'Invalid password', wrong_password_response.data)
        # Testing for invalid password
        wrong_creds_response = self.app.post(self.url_prefix + 'auth/login', data={
            'email': 'anyemail',
            'password': 'anyinvalidpassword'
        })
        self.assertEqual(wrong_creds_response.status_code, 401)
        self.assertIn(b'Invalid email or password', wrong_creds_response.data)
        response = self.app.post(self.url_prefix + 'auth/login', data={
            'email': self.sample_user['email'],
            'password': self.sample_user['password']
        })
        # Test registration with incomplete data
        incomplete_data_response = self.app.post(self.url_prefix + 'auth/login', data={
            'email': 'dummy@dummy.com',
        })
        self.assertEqual(incomplete_data_response.status_code, 400)
        self.assertIn(b'Please provide', incomplete_data_response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'successfully logged', response.data)

if __name__ == '__main__':
    unittest.main()
