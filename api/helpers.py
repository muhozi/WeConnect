from flask import current_app as app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


def get_token(user_id):
    """" Generate token helper function"""
    print(app.config['SECRET_KEY'])
    token = Serializer(app.config['SECRET_KEY'], expires_in=36000)
    token_with_id = token.dumps({'id': user_id})
    return token_with_id.decode('ascii')
