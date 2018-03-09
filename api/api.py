"""
    Our Main api app
"""
import uuid
from functools import wraps
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from api.models.store import Store
from api.models.user import User
from api.models.business import Business
from api.inputs.inputs import validate, REGISTER_RULES, LOGIN_RULES, RESET_PWD_RULES, REGISTER_BUSINESS_RULES
from api.helpers import get_token, token_id

API = Blueprint('api', 'api', url_prefix='/api/v1/')
STORE = Store


def auth(arg):
    """ Auth middleware to check logged in user"""
    @wraps(arg)
    def wrap(*args, **kwargs):
        """ Check if token exists in the request header"""
        if request.headers.get('Authorization'):
            token = request.headers.get('Authorization')
            if User.token_exists(token) and token_id(token):
                print(token_id(token))
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
    valid = validate(request.form, REGISTER_RULES)
    if valid != True:
        response = jsonify(
            status='error', message="Please provide valid details", errors=valid)
        response.status_code = 400
        return response
    data = {
        'id': uuid.uuid4().hex,
        'username': request.form['username'],
        'email': request.form['email'],
        'password': request.form['password'],
    }
    if User.user_exists(data['email']):
        response = jsonify({
            'status': 'error',
            'message': "Sorry the email address has been taken"
        })
        response.status_code = 400
        return response
    User.save(data)
    response = jsonify({
        'status': 'ok',
        'message': "You have been successfully registered"
    })
    response.status_code = 201
    return response


@API.route('auth/logout', methods=['POST'])
@auth
def logout():
    """
        Logout endpoint
    """
    Store.remove_token(request.headers.get('Authorization'))
    response = jsonify({
        'status': 'ok',
        'message': "You have successfully logged out"
    })
    response.status_code = 200
    return response


@API.route('auth/login', methods=['POST'])
def login():
    """
        Login endpoint method
    """
    valid = validate(request.form, LOGIN_RULES)
    if valid != True:
        response = jsonify(
            status='error', message="Please provide valid details", errors=valid)
        response.status_code = 400
        return response
    data = {
        'email': request.form['email'],
        'password': request.form['password'],
    }
    # Check if email exists in the store
    logged_user = User.get_user(data['email'])
    if logged_user:
        # Check password
        if check_password_hash(logged_user['password'], data['password']):
            token = get_token(logged_user['id'])
            User.add_token(token)
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


@API.route('auth/reset-password', methods=['POST'])
@auth
def reset_password():
    """
        Registration endpoint method
    """
    valid = validate(request.form, RESET_PWD_RULES)
    if valid != True:
        response = jsonify(status='error', message=valid)
        response.status_code = 400
        return response
    user_id = token_id(request.headers.get('Authorization'))
    if User.check_password(user_id, request.form['old_password']) != True:
        response = jsonify({
            'status': 'error',
            'message': "Invalid old password"
        })
        response.status_code = 400
        return response
    User.change_password(user_id, request.form['new_password'])
    response = jsonify({
        'status': 'ok',
        'message': "You have successfully changed your password"
    })
    response.status_code = 201
    return response


@API.route('businesses', methods=['POST'])
@auth
def register_business():
    """
        Business registration endpoint endpoint method
    """
    valid = validate(request.form, REGISTER_BUSINESS_RULES)
    if valid != True:
        response = jsonify(
            status='error', message="Please provide required info", errors=valid)
        response.status_code = 400
        return response
    user_id = token_id(request.headers.get('Authorization'))
    data = {
        'id': uuid.uuid4().hex,
        'user_id': user_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'country': request.form['country'],
        'city': request.form['city'],
    }
    if(Business.has_same_business(user_id, request.form['name'])):
        response = jsonify(
            status='error', message="You have already registered this business")
        response.status_code = 400
        return response
    Business.save(data)
    response = jsonify({
        'status': 'ok',
        'message': "Your business has been successfully registered"
    })
    response.status_code = 201
    return response


@API.route('businesses/<id>', methods=['DELETE'])
@auth
def delete_business(id):
    """
        Business deletion endpoint method
    """
    user_id = token_id(request.headers.get('Authorization'))
    if(Business.has_this_business(user_id, id)):
        Business.delete_business(id)
        response = jsonify({
            'status': 'ok',
            'message': "Your business has been successfully deleted"
        })
        response.status_code = 202
        return response
    response = jsonify(
        status='error', message="This business doesn't exist")
    response.status_code = 400
    return response


@API.route('businesses/<id>', methods=['PUT'])
@auth
def update_business(id):
    """
        Business updating endpoint method
    """
    user_id = token_id(request.headers.get('Authorization'))
    if(Business.has_this_business(user_id, id)):
        valid = validate(request.form, REGISTER_BUSINESS_RULES)
        if valid != True:
            response = jsonify(
                status='error', message="Please provide required info", errors=valid)
            response.status_code = 400
            return response
        data = {
            'user_id': user_id,
            'name': request.form['name'],
            'description': request.form['description'],
            'country': request.form['country'],
            'city': request.form['city'],
        }
        if(Business.has_two_same_business(user_id, request.form['name'], id)):
            response = jsonify(
                status='error', message="You have already registered this other business with same name")
            response.status_code = 400
            return response
        Business.update(id, data)
        response = jsonify({
            'status': 'ok',
            'message': "Your business has been successfully updated"
        })
        response.status_code = 202
        return response
    response = jsonify(
        status='error', message="This business doesn't exist")
    response.status_code = 400
    return response

@API.route('businesses', methods=['GET'])
@auth
def get_user_businesses():
    """
        Business updating endpoint method
    """
    user_id = token_id(request.headers.get('Authorization'))
    if(Business.has_business(user_id)):
        businesses = Business.user_businesses(user_id)
        response = jsonify({
            'status': 'ok',
            'message': 'You have businesses'+ str(len(businesses)) +'registered businesses',
            'businesses': businesses
        })
        response.status_code = 200
        return response
    response = jsonify(
        status='error', message="You don't have registered business")
    response.status_code = 400
    return response
