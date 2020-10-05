import os
from dotenv import load_dotenv

base_dir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(base_dir,'.env'),encoding='utf-8')

class BaseConfig:

    DEBUG = True
    SQLALCHEMY_DATABASE_URI='mysql://root:@localhost:3306/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass


config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig
}
