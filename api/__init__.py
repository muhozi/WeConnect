"""
	 Initialize the app
"""
from flask import Flask
from api.api import API
APP = Flask(__name__, instance_relative_config=True)
APP.register_blueprint(API)


def create_app():
    """Init the app"""
    return APP
APP.config.from_object('config')
