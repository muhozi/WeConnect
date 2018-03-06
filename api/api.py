"""
    Our Main api app
"""
import uuid
from flask import Blueprint, jsonify, request
from functools import wraps
from werkzeug.security import check_password_hash
from api.models.store import store
from api.models.user import user
from api.inputs.inputs import register_inputs, login_inputs
from api.helpers import get_token

api = Blueprint('api', 'api', url_prefix='/api/v1/')
store = store()


def auth(n):
    """ Auth middleware to check logged in user"""
    @wraps(n)
    def wrap(*args, **kwargs):
        if request.headers.get('Authorization'):
            token = request.headers.get('Authorization')
            if user().token_exists(token):
                return n(*args, **kwargs)
        response = jsonify({
            'status': 'error',
            'message': "Unauthorized"
        })
        response.status_code = 401
        return response
    return wrap


@api.route('auth/register', methods=['POST'])
def register():
    """
        Registration endpoint method
    """
    inputs = register_inputs()
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
    if user().user_exists(data['email']):
        response = jsonify({
            'status': 'error',
            'message': "Sorry the email address has been taken"
        })
        response.status_code = 400
        return response
    user().save(data)
    response = jsonify({
        'status': 'ok',
        'message': "You have been successfully registered"
    })
    response.status_code = 200
    return response


@api.route('auth/login', methods=['POST'])
def login():
    """
        Login endpoint method
    """
    inputs = login_inputs()
    if not inputs.validate(request.form):
        response = jsonify(status='error', message=inputs.error)
        response.status_code = 400
        return response
    data = {
        'email': request.form['email'],
        'password': request.form['password'],
    }
    # Check if email exists in the store
    logged_user = user().get_user(data['email'])
    if logged_user:
        # Check password
        if check_password_hash(logged_user['password'], data['password']):
            token = get_token(logged_user['id'])
            user().add_token(token)
            response = jsonify({
                'status': 'ok',
                'token': token,
                'message': "You have been successfully logged in"
            })
            response.status_code = 200
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
