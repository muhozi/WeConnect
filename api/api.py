"""
    Our Main api routes
"""
import datetime
import uuid
from functools import wraps
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from flasgger.utils import swag_from
from api.models.store import Store
from api.models.user import User
from api.models.business import Business
from api.models.review import Review
from api.docs.docs import (REGISTER_DOCS,
                           LOGIN_DOCS,
                           LOGOUT_DOCS,
                           RESET_PASSWORD_DOCS,
                           REGISTER_BUSINESS_DOCS,
                           GET_BUSINESSES_DOCS,
                           UPDATE_BUSINESS_DOCS,
                           DELETE_BUSINESS_DOCS,
                           BUSINESS_REVIEWS_DOCS,
                           ADD_BUSINESS_REVIEW_DOCS,
                           GET_BUSINESS_DOCS)
from api.inputs.inputs import (
    validate, REGISTER_RULES, LOGIN_RULES, RESET_PWD_RULES,
    REGISTER_BUSINESS_RULES, REVIEW_RULES)
from api.helpers import get_token, token_id

API = Blueprint('v1', __name__, url_prefix='/api/v1')
STORE = Store


def auth(arg):
    """ Auth middleware to check logged in user"""
    @wraps(arg)
    def wrap(*args, **kwargs):
        """ Check if token exists in the request header"""
        if request.headers.get('Authorization'):
            token = request.headers.get('Authorization')
            if User.token_exists(token) and token_id(token):
                return arg(*args, **kwargs)
        response = jsonify({
            'status': 'error',
            'message': "Unauthorized"
        })
        response.status_code = 401
        return response
    return wrap


@API.route('/auth/register', methods=['POST'])
@swag_from(REGISTER_DOCS)
def register():
    """
        User Registration
    """
    valid = validate(request.get_json(force=True), REGISTER_RULES)
    sent_data = request.get_json(force=True)
    if valid != True:
        response = jsonify(
            status='error', message="Please provide valid details", errors=valid)
        response.status_code = 400
        return response
    data = {
        'id': uuid.uuid4().hex,
        'username': sent_data['username'],
        'email': sent_data['email'],
        'password': sent_data['password'],
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


@API.route('/auth/logout', methods=['POST'])
@auth
@swag_from(LOGOUT_DOCS)
def logout():
    """
        User logout
    """
    Store.remove_token(request.headers.get('Authorization'))
    response = jsonify({
        'status': 'ok',
        'message': "You have successfully logged out"
    })
    response.status_code = 200
    return response


@API.route('/auth/login', methods=['POST'])
@swag_from(LOGIN_DOCS)
def login():
    """
        User login
    """
    sent_data = request.get_json(force=True)
    valid = validate(sent_data, LOGIN_RULES)
    if valid != True:
        response = jsonify(
            status='error', message="Please provide valid details", errors=valid)
        response.status_code = 400
        return response
    data = {
        'email': sent_data['email'],
        'password': sent_data['password'],
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
                'message': 'You have been successfully logged in',
                'access_token': token,
            })
            response.status_code = 200
            # response.headers['auth_token'] = token
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


@API.route('/auth/reset-password', methods=['POST'])
@auth
@swag_from(RESET_PASSWORD_DOCS)
def reset_password():
    """
        User password reset
    """
    sent_data = request.get_json(force=True)
    valid = validate(sent_data, RESET_PWD_RULES)
    if valid != True:
        response = jsonify(status='error',
                           message="Please provide valid details",
                           errors=valid)
        response.status_code = 400
        return response
    user_id = token_id(request.headers.get('Authorization'))
    if User.check_password(user_id, sent_data['old_password']) != True:
        response = jsonify({
            'status': 'error',
            'message': "Invalid old password"
        })
        response.status_code = 400
        return response
    User.change_password(user_id, sent_data['new_password'])
    response = jsonify({
        'status': 'ok',
        'message': "You have successfully changed your password"
    })
    response.status_code = 201
    return response


@API.route('/businesses', methods=['POST'])
@auth
@swag_from(REGISTER_BUSINESS_DOCS)
def register_business():
    """
        Register business
    """
    sent_data = request.get_json(force=True)
    valid = validate(sent_data, REGISTER_BUSINESS_RULES)
    if valid != True:
        response = jsonify(
            status='error', message="Please provide required info", errors=valid)
        response.status_code = 400
        return response
    user_id = token_id(request.headers.get('Authorization'))
    data = {
        'id': uuid.uuid4().hex,
        'user_id': user_id,
        'name': sent_data['name'],
        'description': sent_data['description'],
        'country': sent_data['country'],
        'city': sent_data['city'],
    }
    if Business.has_same_business(user_id, sent_data['name']):
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


@API.route('/businesses/<business_id>', methods=['DELETE'])
@auth
@swag_from(DELETE_BUSINESS_DOCS)
def delete_business(business_id):
    """
        Delete business
    """
    user_id = token_id(request.headers.get('Authorization'))
    if Business.has_this_business(user_id, business_id):
        Business.delete_business(business_id)
        response = jsonify({
            'status': 'ok',
            'message': "Your business has been successfully deleted"
        })
        response.status_code = 202
        return response
    response = jsonify(
        status='error',
        message="This business doesn't exist or you don't have privileges to it")
    response.status_code = 400
    return response


@API.route('/businesses/<business_id>', methods=['PUT'])
@auth
@swag_from(UPDATE_BUSINESS_DOCS)
def update_business(business_id):
    """
        Update business
    """
    sent_data = request.get_json(force=True)
    user_id = token_id(request.headers.get('Authorization'))
    if Business.has_this_business(user_id, business_id):
        valid = validate(sent_data, REGISTER_BUSINESS_RULES)
        if valid != True:
            response = jsonify(
                status='error', message="Please provide required info", errors=valid)
            response.status_code = 400
            return response
        data = {
            'user_id': user_id,
            'name': sent_data['name'],
            'description': sent_data['description'],
            'country': sent_data['country'],
            'city': sent_data['city'],
        }
        if Business.has_two_same_business(user_id, sent_data['name'], business_id):
            response = jsonify(
                status='error',
                message="You have already registered this other business with same name")
            response.status_code = 400
            return response
        Business.update(business_id, data)
        response = jsonify({
            'status': 'ok',
            'message': "Your business has been successfully updated"
        })
        response.status_code = 202
        return response
    response = jsonify(
        status='error',
        message="This business doesn't exist or you don't have privileges to it")
    response.status_code = 400
    return response


@API.route('/businesses', methods=['GET'])
@auth
@swag_from(GET_BUSINESSES_DOCS)
def get_user_businesses():
    """
        Business lists
    """
    user_id = token_id(request.headers.get('Authorization'))
    if Business.has_business(user_id):
        businesses = Business.user_businesses(user_id)
        response = jsonify({
            'status': 'ok',
            'message': 'You have businesses ' + str(len(businesses)) + ' registered businesses',
            'businesses': businesses
        })
        response.status_code = 200
        return response
    response = jsonify(
        status='error', message="You don't have registered business")
    response.status_code = 204
    return response


@API.route('/businesses/<business_id>', methods=['GET'])
@swag_from(GET_BUSINESS_DOCS)
def get_business(business_id):
    """
        Get business
    """
    if business_id in [business['id'] for business in Store.businesses]:
        business = Business.get_business(
            business_id)  # Get business details
        response = jsonify({
            'status': 'ok',
            'message': 'Business found',
            'business': business,
        })
        response.status_code = 200
        return response
    response = jsonify({
        'status': 'error',
        'message': "Business not found"
    })
    response.status_code = 400
    return response


@API.route('/businesses/<business_id>/reviews', methods=['POST'])
@auth
@swag_from(ADD_BUSINESS_REVIEW_DOCS)
def add_business_review(business_id):
    """
        Add Review
    """
    if business_id in [business['id'] for business in Store.businesses]:
        sent_data = request.get_json(force=True)
        valid = validate(sent_data, REVIEW_RULES)
        if valid != True:
            response = jsonify(
                status='error', message='Please provide valid details', errors=valid)
            response.status_code = 400
            return response
        user_id = token_id(request.headers.get('Authorization'))
        data = {
            'id': uuid.uuid4().hex,
            'user_id': user_id,
            'review': sent_data['review'],
            'created_at': f"{datetime.datetime.now():%Y-%m-%d %H:%M}",
        }
        Review.save(business_id, data)
        response = jsonify({
            'status': 'ok',
            'message': "Your review has been submitted"
        })
        response.status_code = 201
        return response
    response = jsonify({
        'status': 'error',
        'message': "This business doesn't exist"
    })
    response.status_code = 400
    return response


@API.route('/businesses/<business_id>/reviews', methods=['GET'])
@swag_from(BUSINESS_REVIEWS_DOCS)
def get_business_reviews(business_id):
    """
        Business reviews
    """
    if business_id in [business['id'] for business in Store.businesses]:
        if business_id in Store.reviews:
            reviews = Store.reviews[business_id]
            business = Business.get_business(
                business_id)  # Get business details
            response = jsonify({
                'status': 'ok',
                'message': str(len(reviews)) + " reviews found",
                'business': business,
                'reviews': reviews
            })
            response.status_code = 200
            return response
        response = jsonify({
            'status': 'ok',
            'message': "No business review yet"
        })
        response.status_code = 204
        return response
    response = jsonify({
        'status': 'error',
        'message': "This business doesn't exist"
    })
    response.status_code = 400
    return response
