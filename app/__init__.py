from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# local imports
from config import app_config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)

    from app.route import route
    app.register_blueprint(route)
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    return app
