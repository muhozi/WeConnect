"""
    Helper Methods
"""
from flask import current_app as app
from itsdangerous import (URLSafeTimedSerializer
                          as Serializer, BadSignature, SignatureExpired)


def get_token(user_id, expires_in=3600, key=None):
    """"
        Generate token helper function
    """
    if key is None:
        key = app.config['SECRET_KEY']
    token = Serializer(key, expires_in)
    token_with_id = token.dumps({'id': user_id})
    return token_with_id.decode('ascii')


def token_id(token):
    """
        Check token if token is valid this returns ID aapended to it
    """
    deserialize_token = Serializer(app.config['SECRET_KEY'])
    try:
        data = deserialize_token.loads(token)
    except SignatureExpired:
        return False  # valid token, but expired
    except BadSignature:
        return False  # invalid token
    return data['id']
