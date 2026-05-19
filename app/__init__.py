from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = '請先登入以存取此頁面。'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
