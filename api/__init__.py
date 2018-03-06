from flask import Flask, render_template, request, flash, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from api.api import api
app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(api)

def create_app():
    return app
app.config.from_object('config')