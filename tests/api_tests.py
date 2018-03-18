"""
    Main test
"""
import unittest
import uuid
from api import APP
from flask import json
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
            'id': uuid.uuid4().hex,
            'username': 'Kudo',
            'email': 'kaka@andela.com',
            'password': 'secret',
            'confirm_password': 'secret'
        }
        self.business_data = {
            'id': uuid.uuid4().hex,
            'name': 'Inzora rooftop coffee',
            'description': 'We have best coffee for you,',
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
        # Save business for reviews testing
        self.rev_business_data = {
            'id': uuid.uuid4().hex,
            'name': 'KFC',
            'description': 'Finger lickin\' good',
            'country': 'Kenya',
            'city': 'Nairobi'
        }
        # Add user(owner) to the business data dict
        self.rev_business_data['user_id'] = self.sample_user['id']
        # Save business in the storage list for testing
        Business.save(self.rev_business_data)
        with APP.test_request_context():
            # Orphan id: User id that will be used to create an orphan token
            orphan_id = uuid.uuid4().hex
            save_user.save({
                'id': orphan_id,
                'username': "uname",
                'email': "anyemail@gmail.com",
                'password': self.exist_user['password'],
                'confirm_password': self.exist_user['confirm_password']
            })
            # Issue a token the the test user (sample_user)
            # Store test token in auth storage auth_token list
            token = get_token(self.sample_user['id'])
            #Orphan token: User token that do not have any registered business 
            orphan_token = get_token(orphan_id)
            expired_token = get_token(self.sample_user['id'], -3600)
            User().add_token(token)
            User().add_token(expired_token)
            User().add_token(orphan_token)
            self.test_token = token
            self.expired_test_token = expired_token
            self.orphan_test_token = orphan_token
