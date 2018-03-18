"""
    Main test
"""
import unittest
import uuid
# from api import APP
from flask import json
from api.models.user import User
from api.models.business import Business
from api.helpers import get_token
from tests.api_tests import MainTests


class BusinessTests(MainTests):
    """
        Main test
    """

    def test_business_registration(self):
        '''
            Testing business registration
        '''
        response = self.app.post(self.url_prefix + 'businesses', data=json.dumps({
            'name': 'Inzora rooftop coffee',
            'description': 'We have best coffee',
            'country': 'Kenya',
            'city': 'Nairobi'
        }), headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            b'business has been successfully registered', response.data)

    def test_same_business_registration(self):
        '''
            Test business registration with the same name under same user
        '''
        data = self.business_data
        data['user_id'] = self.sample_user['id']
        Business().save(self.business_data)  # Save business assigned to sample user
        response = self.app.post(self.url_prefix + 'businesses',
                                 data=json.dumps(self.business_data),
                                 headers={'Authorization': self.test_token}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'You have already registered this business', response.data)

    def test_business_with_invalid_data(self):
        '''
            Testing business registration with invalid data
        '''
        response = self.app.post(self.url_prefix + 'businesses', data=json.dumps({
            'description': 'We have best coffee for you, Come and drink it in the best view of the town',
            'country': 'Kenya',
            'city': 'Nairobi'
        }), headers={'Authorization': self.test_token}, content_type='application/json')
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

    def test_no_priv_business_deletion(self):
        '''
            Test removing business without privileges to it
        '''
        # Add user(owner) to the business data dict
        self.business_data['user_id'] = self.sample_user['id']
        # Save business in the storage list for testing
        Business.save(self.business_data)
        response = self.app.delete(self.url_prefix + 'businesses/' + self.business_data[
            'id'], data={}, headers={'Authorization': self.orphan_test_token})
        self.assertEqual(response.status_code, 400)

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
            'id'], data=json.dumps(new_business_data), headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 202)
        self.assertIn(
            b'Your business has been successfully updated', response.data)

    def test_no_priv_business_update(self):
        '''
            Test business updating with no privileges to it
        '''
        # New business details to test updating
        new_business_data = {
            'name': 'Wazi wazi',
            'description': 'Enjoy Coffee and Pizzas',
            'country': 'Kenya',
            'city': 'Nakuru'
        }
        # Add user(owner) to the business data dict
        response = self.app.put(self.url_prefix + 'businesses/' + self.business_data[
            'id'], data=json.dumps(new_business_data), headers={'Authorization': self.orphan_test_token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'This business doesn\'t exist or you don\'t have privileges to it', response.data)

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
        response = self.app.put(self.url_prefix + 'businesses/' +
                                self.business_data['id'], data=json.dumps(
                                    new_business_data),
                                headers={'Authorization': self.test_token}, content_type='application/json')
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
            'id'], data=json.dumps(new_business_data), headers={'Authorization': self.test_token},
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'Please provide required info', response.data)

    def test_no_user_businesses(self):
        '''
            Test retrieving logged in user business without any
        '''
        response = self.app.get(
            self.url_prefix + 'businesses', headers={'Authorization': self.orphan_test_token})
        self.assertEqual(response.status_code, 204)

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

    def test_business(self):
        '''
            Test retrieving business details
        '''
        response = self.app.get(
            self.url_prefix + 'businesses/' + self.rev_business_data['id'], headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Business found', response.data)

    def test_non_exist_business(self):
        '''
            Test retrieving business details which doesn't exist
        '''
        response = self.app.get(
            self.url_prefix + 'businesses/' + "fsdfsd", headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'Business not found', response.data)
