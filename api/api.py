from flask import Blueprint, request, jsonify,request
from api.models.store import store
from api.models.user import user

api = Blueprint('api', 'api', url_prefix='/api/v1/')
store = store()
@api.route('auth/register',methods = ['POST'])
def register():
	# user().save();
    return jsonify({
    	'message':'You have been successfully registered'
    })
"""
    Logout route
"""
@api.route('auth/login',methods = ['POST'])
# @auth
def login():
    # Look for token and delete in the storage
    return jsonify({
    	'message':'welcome'
    })