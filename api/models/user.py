""" User Model """

from werkzeug.security import generate_password_hash
from api.models.store import Store


class User(object):
    """Users Model"""

    def save(self, data):
        """ Save user in the main store """
        data['password'] = generate_password_hash(data['password'])
        Store().save_user(data)

    def user_exists(self, email):
        """Check if user exists """
        for user_ in Store().users:
            if user_['email'] == email:
                return True
        return False

    def get_user(self, email):
        """Check if user exists and return user details"""
        for user_ in Store().users:
            if user_['email'] == email:
                return user_
        return False

    def add_token(self, token):
        """ Add token in the main store """
        Store().save_token(token)

    def token_exists(self, user_token):
        """Check if user exists """
        for token in Store().auth_tokens:
            if token == user_token:
                return True
        return False
