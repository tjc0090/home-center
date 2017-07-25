import os

from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from pymongo import MongoClient

from config import app_config

login_manager = LoginManager()
UPLOAD_PATH = 'app/static/uploads'
#need to add user loader (models.py for example)

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config["UPLOAD_PATH"] = UPLOAD_PATH

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to view that page"
    login_manager.login_view = "auth.login"

    Bootstrap(app)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/admin")

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    return app
