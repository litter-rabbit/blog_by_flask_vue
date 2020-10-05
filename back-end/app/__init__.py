
from flask import Flask

from config import config


def create_app(configname=None):

    app=Flask(__name__)
    app.config.from_object(config[configname])
    register_blueprints(app)
    return app



def register_blueprints(app):
    from app.api import api_bp
    app.register_blueprint(api_bp,url_prefix='/api')




