"""
	 Initialize the app
"""
from flask import Flask
from flasgger import Swagger
from api.api import API
APP = Flask(__name__, instance_relative_config=True)
APP.register_blueprint(API)
SWAGGER_CONFIG = {
    "headers":[],
    "title": "WeConnect",
    "specs": [
        {
            "version": "1",
            "title": "Api v1",
            "endpoint": 'apispec',
            "route": '/api/v1/docs.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/swagger_files",
    "swagger_ui": True,
    "specs_route": "/api/v1"
}
TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "WeConnect",
        "description": "WeConnect Platform API v1",
        "version": "1"
    },
    "consumes": [
        "application/json",
    ],
    "produces": [
        "application/json",
    ],
    "schemes": [
        "http",
        "https"
    ],
    "operationId": "getmyData"
}

SWAGGER = Swagger(APP, config=SWAGGER_CONFIG, template=TEMPLATE)

APP.config.from_object('config')
