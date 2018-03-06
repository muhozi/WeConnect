""" User Model """

from werkzeug.security import generate_password_hash
from api.models.store import store


class user(object):
    """Users Model"""

    def save(self, data):
        """ Save user in the main store """
        data['password'] = generate_password_hash(data['password'])
        store().save_user(data)

    def user_exists(self, email):
        """Check if user exists """
        for user_ in store().users:
            if user_['email'] == email:
                return True
        return False

    def get_user(self, email):
        """Check if user exists and return user details"""
        for user_ in store().users:
            if user_['email'] == email:
                return user_
        return False

    def add_token(self, token):
        """ Add token in the main store """
        store().save_token(token)
