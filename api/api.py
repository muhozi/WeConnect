"""
    Our Main api app
"""
import uuid
from functools import wraps
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from api.models.store import Store
from api.models.user import User
from api.inputs.inputs import RegisterInputs, LoginInputs
from api.helpers import get_token

API = Blueprint('api', 'api', url_prefix='/api/v1/')
STORE = Store()


def auth(arg):
    """ Auth middleware to check logged in user"""
    @wraps(arg)
    def wrap(*args, **kwargs):
        """ Check if token exists in the request header"""
        if request.headers.get('Authorization'):
            token = request.headers.get('Authorization')
            if User().token_exists(token):
                return arg(*args, **kwargs)
        response = jsonify({
            'status': 'error',
            'message': "Unauthorized"
        })
        response.status_code = 401
        return response
    return wrap


@API.route('auth/register', methods=['POST'])
def register():
    """
        Registration endpoint method
    """
    inputs = RegisterInputs()
    if not inputs.validate(request.form):
        response = jsonify(status='error', message=inputs.error)
        response.status_code = 400
        return response
    data = {
        'id': uuid.uuid4().hex,
        'names': request.form['names'],
        'email': request.form['email'],
        'password': request.form['password'],
    }
    if User().user_exists(data['email']):
        response = jsonify({
            'status': 'error',
            'message': "Sorry the email address has been taken"
        })
        response.status_code = 400
        return response
    User().save(data)
    response = jsonify({
        'status': 'ok',
        'message': "You have been successfully registered"
    })
    response.status_code = 201
    return response


@API.route('auth/login', methods=['POST'])
def login():
    """
        Login endpoint method
    """
    inputs = LoginInputs()
    if not inputs.validate(request.form):
        response = jsonify(status='error', message=inputs.error)
        response.status_code = 400
        return response
    data = {
        'email': request.form['email'],
        'password': request.form['password'],
    }
    # Check if email exists in the store
    logged_user = User().get_user(data['email'])
    if logged_user:
        # Check password
        if check_password_hash(logged_user['password'], data['password']):
            token = get_token(logged_user['id'])
            User().add_token(token)
            response = jsonify({
                'status': 'ok',
                'message': "You have been successfully logged in"
            })
            response.status_code = 200
            response.headers['auth_token'] = token
            return response
        response = jsonify({
            'status': 'error',
            'message': "Invalid password"
        })
        response.status_code = 401
        return response
    response = jsonify({
        'status': 'error',
        'message': "Invalid email or password"
    })
    response.status_code = 401
    return response
