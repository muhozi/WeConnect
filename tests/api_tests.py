"""
    Main test
"""
import unittest
import uuid
from api import APP
from api.models.user import User
from api.models.business import Business
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
            'username': 'Muhozi',
            'email': 'emery@andela.com',
            'password': 'secret',
            'confirm_password': 'secret'
        }
        self.exist_user = {
            'username': 'Kudo',
            'email': 'kaka@andela.com',
            'password': 'secret',
            'confirm_password': 'secret'
        }
        self.business_data = {
            'id': uuid.uuid4().hex,
            'name': 'Inzora rooftop coffee',
            'description': 'We have best coffee for you, Come and drink it in the best view of the town',
            'country': 'Kenya',
            'city': 'Nairobi'
        }
        save_user = User()
        save_user.save({
            'id': self.sample_user['id'],
            'username': self.sample_user['username'],
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
            'username': self.exist_user['username'],
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
            'username': self.exist_user['username'],
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
            'username': 'dummy name',
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

    def test_logout(self):
        """
            Test Logout
        """
        response = self.app.post(self.url_prefix + 'auth/logout',
                                 data={}, headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have successfully logged out', response.data)

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

    def test_valid_token(self):
        """
            Testing valid token
        """
        # Test invalid token by accessing protected endpoint with invalid
        # authorization token
        response = self.app.post(self.url_prefix + 'auth/reset-password', data={
            'old_password': self.sample_user['password'],  # Old password
            'new_password': '123456',
        },
            headers={'Authorization': 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyMDUzMzQyOSwiZXhwIjoxNTIwNTY5NDI5fQ.eyJpZCI6ImQ1NDlmZGM3NNkNzQ2N2RhOGYwYmFiMjUxMjNjNjc5In0.yQ4yQxZYI-vmeqW6s1hqaC3OrXuii_D8mK2lpEcDn7g'})
        self.assertEqual(response.status_code, 401)
        self.assertIn(
            b'Unauthorized', response.data)

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
            Test business registration with the same name under same user
        '''
        data = self.business_data
        data['user_id'] = self.sample_user['id']
        Business().save(self.business_data)  # Save business assigned to sample user
        response = self.app.post(self.url_prefix + 'businesses',
                                 data=self.business_data, headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'You have already registered this business', response.data)

    def test_business_with_invalid_data(self):
        '''
            Testing business registration with invalid data
        '''
        response = self.app.post(self.url_prefix + 'businesses', data={
            'description': 'We have best coffee for you, Come and drink it in the best view of the town',
            'country': 'Kenya',
            'city': 'Nairobi'
        }, headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'Please provide required info', response.data)

    def test_business_deletion(self):
        '''
            Test removing business
        '''
        # Add user(owner) to the business data dict
        self.business_data['user_id'] = self.sample_user['id']
        # Save business in the storage list for testing
        Business.save(self.business_data)
        response = self.app.delete(self.url_prefix + 'businesses/' + self.business_data[
                                   'id'], data={}, headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 202)
        self.assertIn(
            b'Your business has been successfully deleted', response.data)

    def test_business_update(self):
        '''
            Test business updating
        '''
        # New business details to test updating
        new_business_data = {
            'name': 'Inzora Nakuru',
            'description': 'Enjoy Coffee and Pizzas',
            'country': 'Kenya',
            'city': 'Nakuru'
        }
        # Add user(owner) to the business data dict
        self.business_data['user_id'] = self.sample_user['id']
        # Save business in the storage list for testing
        Business.save(self.business_data)
        response = self.app.put(self.url_prefix + 'businesses/' + self.business_data[
            'id'], data=new_business_data, headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 202)
        self.assertIn(
            b'Your business has been successfully updated', response.data)

    def test_updating_business_with_same_name(self):
        '''
            Test business updating with existing busiiness name under one user
        '''
        # New business details to test updating
        new_business_data = {
            'name': 'TRM',
            'description': 'Enjoy Coffee and Pizzas',
            'country': 'Kenya',
            'city': 'Nakuru'
        }
        # Data to be saved to test same name businesses under one person
        additional_business_data = {
            'id': uuid.uuid4().hex,
            'user_id': self.sample_user['id'],
            'name': 'TRM',
            'description': 'Enjoy Coffee and Pizzas',
            'country': 'Kenya',
            'city': 'Nakuru'
        }
        # Add user(owner) to the business data dict
        self.business_data['user_id'] = self.sample_user['id']
        # Save business in the storage list for testing
        Business.save(self.business_data)
        Business.save(additional_business_data)
        response = self.app.put(self.url_prefix + 'businesses/' + self.business_data[
            'id'], data=new_business_data, headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'You have already registered this other business with same name', response.data)

    def test_business_update_with_invalid_data(self):
        '''
            Test business updating with invalid data
        '''
        # New business details to test updating
        new_business_data = {
            'name': 'Inzora Nakuru',
            'country': 'Kenya',
            'city': 'Nakuru'
        }
        # Add user(owner) to the business data dict
        self.business_data['user_id'] = self.sample_user['id']
        # Save business in the storage list for testing
        Business.save(self.business_data)
        response = self.app.put(self.url_prefix + 'businesses/' + self.business_data[
            'id'], data=new_business_data, headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'Please provide required info', response.data)

    def test_businesses(self):
        '''
            Test retrieving logged in user business
        '''
        # New business details to test updating
        dummy_business_data = {
            'id': uuid.uuid4().hex,
            'user_id': self.sample_user['id'],
            'name': 'KFC',
            'description': 'Finger lickin\' good',
            'country': 'Kenya',
            'city': 'Nairobi'
        }
        # Add user(owner) to the business data dict
        self.business_data['user_id'] = self.sample_user['id']
        # Save businesses to test
        Business.save(self.business_data)
        Business.save(dummy_business_data)
        response = self.app.get(
            self.url_prefix + 'businesses', headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
