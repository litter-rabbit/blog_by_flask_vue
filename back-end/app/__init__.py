
from flask import Flask

from config import config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click


db=SQLAlchemy()
migrate = Migrate()

def create_app(configname=None):

    app=Flask(__name__)
    app.config.from_object(config[configname])
    CORS(app)
    db.init_app(app)
    migrate.init_app(app,db)
    register_blueprints(app)
    register_command(app)

    return app



def register_blueprints(app):
    from app.api import api_bp
    app.register_blueprint(api_bp,url_prefix='/api')


def  register_command(app):
    @app.cli.command()
    @click.option('--drop',is_flag=True,help='create after drop')
    def initdb(drop):

        if drop:
            click.confirm('this operation  will drop database?',abort=True)
            db.drop_all()
            click.echo('drop table')
        db.create_all()
        click.echo('initialized success')






from app import modles



