from flask import Blueprint, request, jsonify,request
import uuid
from api.models.store import store
from api.models.user import user
from werkzeug.security import generate_password_hash, check_password_hash
from api.inputs.inputs import RegisterInputs,LoginInputs

api = Blueprint('api', 'api', url_prefix='/api/v1/')
store = store()
@api.route('auth/register',methods = ['POST'])
def register():
    inputs = RegisterInputs()
    if not inputs.validate(request.form):
        response = jsonify(status='error', message=inputs.error)
        response.status_code = 400
        return response
    data = {
        'id':uuid.uuid4().hex,
        'names':request.form['names'],
        'email':request.form['email'],
        'password':generate_password_hash(request.form['password']),
    }
    if (user().user_exists(data['email'])):
        response = jsonify({
            'status':'error',
            'message':"Sorry the email address has been taken"
        })
        response.status_code = 400
        return response
    user().save(data)
    response = jsonify({
        'status':'ok',
        'message':"You have been successfully registered"
    })
    response.status_code = 200
    return response
"""
    login Endpoints
"""
@api.route('auth/login',methods = ['POST'])
# @auth
def login():
    pass