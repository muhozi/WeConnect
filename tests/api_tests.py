"""
    Main test
"""
import unittest
import uuid
from api import APP
from api.models.user import User
from api.helpers import get_token


class MainTests(unittest.TestCase):
    """
        Main test
    """
    url_prefix = '/api/v1/'

    def setUp(self):
        """
            Set up test data
        """
        self.app = APP.test_client()
        self.app.testing = True

        self.sample_user = {
            'id': uuid.uuid4().hex,
            'names': 'Muhozi',
            'email': 'emery@andela.com',
            'password': 'secret',
            'confirm_password': 'secret'
        }
        self.exist_user = {
            'names': 'Kudo',
            'email': 'kaka@andela.com',
            'password': 'secret',
            'confirm_password': 'secret'
        }
        save_user = User()
        save_user.save({
            'id': self.sample_user['id'],
            'names': self.sample_user['names'],
            'email': self.sample_user['email'],
            'password': self.sample_user['password'],
            'confirm_password': self.sample_user['confirm_password']
        })
        with APP.test_request_context():
            # Issue a token the the test user (smaple_user)
            token = get_token(self.sample_user['id'])
            # Store test token in auth storage auth_token list
            User().add_token(get_token(self.sample_user['id']))
            self.test_token = get_token(self.sample_user['id'])

    def test_registration(self):
        '''
            Testing registration
        '''
        response = self.app.post(self.url_prefix + 'auth/register', data={
            'names': self.exist_user['names'],
            'email': self.exist_user['email'],
            'password': self.exist_user['password'],
            'confirm_password': self.exist_user['confirm_password']
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'have been successfully registered', response.data)

    def test_exist_email(self):
        '''
            Testing registration with exist email
        '''
        response = self.app.post(self.url_prefix + 'auth/register', data={
            'names': self.exist_user['names'],
            'email': self.sample_user['email'],
            'password': self.exist_user['password'],
            'confirm_password': self.exist_user['confirm_password']
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Sorry the email address has been taken', response.data)

    def test_wrong_registration(self):
        """
            Test registration with incomplete data
        """
        response = self.app.post(self.url_prefix + 'auth/register', data={
            'names': 'dummy name',
            'confirm_password': self.exist_user['confirm_password']
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Please provide', response.data)

    def test_login(self):
        """
            Testing login
        """
        response = self.app.post(self.url_prefix + 'auth/login', data={
            'email': self.sample_user['email'],
            'password': self.sample_user['password']
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'successfully logged', response.data)

    def test_invalid_password(self):
        """
            Testing for invalid password
        """
        response = self.app.post(self.url_prefix + 'auth/login', data={
            'email': self.sample_user['email'],
            'password': 'anyinvalidpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid password', response.data)

    def test_invalid_credentials(self):
        """
            Testing for invalid credentials
        """
        response = self.app.post(self.url_prefix + 'auth/login', data={
            'email': 'anyemail',
            'password': 'anyinvalidpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid email or password', response.data)

    def test_incomplete_creds(self):
        """
            Test registration with incomplete data
        """
        response = self.app.post(self.url_prefix + 'auth/login', data={
            'email': 'dummy@dummy.com',
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Please provide', response.data)

    def test_password_reset(self):
        """
            Testing password Reset
        """
        response = self.app.post(self.url_prefix + 'auth/reset-password', data={
            'old_password': self.sample_user['password'],  # Old password
            'new_password': '123456',
        },
            headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            b'You have successfully changed your password', response.data)

    def test_business_registration(self):
        '''
            Testing business registration
        '''
        response = self.app.post(self.url_prefix + 'businesses', data={
            'name': 'Inzora rooftop coffee',
            'description': 'We have best coffee for you, Come and drink it in the best view of the town',
            'country': 'Kenya',
            'city': 'Nairobi'
        }, headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            b'business has been successfully registered', response.data)

    def test_business_owner_business_registration(self):
        '''
            Testing business registration with by existing business owner
        '''
        response = self.app.post(self.url_prefix + 'businesses', data={
            'name': 'Inzora rooftop coffee',
            'description': 'We have best coffee for you, Come and drink it in the best view of the town',
            'country': 'Kenya',
            'city': 'Nairobi'
        }, headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            b'You have already registered business', response.data)

    def test_business_with_invalid_data(self):
        '''
            Testing business registration with invalid data
        '''
        response = self.app.post(self.url_prefix + 'businesses', data={
            'description': 'We have best coffee for you, Come and drink it in the best view of the town',
            'country': 'Kenya',
            'city': 'Nairobi'
        }, headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            b'Please provide required info', response.data)

if __name__ == '__main__':
    unittest.main()
