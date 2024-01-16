import os
from app.config.connection_configuration import session,engine
basedir = os.path.abspath(os.path.dirname(__file__))

class Config :
    SECRET_KEY = os.environ.get['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = str(engine.url)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
