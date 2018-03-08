""" User Model """

from werkzeug.security import generate_password_hash, check_password_hash
from api.models.store import Store


class User(Store):
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

    def check_password(self, id, readable_password):
        """ Check if password """
        for user in Store().users:
            if user['id'] == id:
                if check_password_hash(user['password'], readable_password):
                    return True
        return False

    def change_password(self, id, password):
        """ Update user password """
        password = generate_password_hash(password)
        Store().update_password(id, password)

    def has_business(self, user_id):
        """Check if user has business """
        for user_ in Store().businesses:
            if user_['user_id'] == user_id:
                return True
        return False
