"""
    config
    ~~~~~~

    Application configurations.
"""
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    APP_NAME = 'social'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///{}'.format(os.path.join(basedir, 'social.db'))
    """
    SQLALCHEMY_DATABASE_URI = 'mysql://social:testing@localhost/social'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['onosendi']


class DefaultConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass
