"""
    config
    ~~~~~~

    Application configurations.
"""
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///{}'.format(os.path.join(basedir, 'social.db'))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DefaultConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    pass
