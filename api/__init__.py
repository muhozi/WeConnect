"""
	 Initialize the app
"""
from flask import Flask
from api.api import api
app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(api)


def create_app():
    """Init the app"""
    return app
app.config.from_object('config')
