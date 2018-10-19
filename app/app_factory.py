"""
    app.app
    ~~~~~~~

    Flask application factory.
"""
import os
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from flask import Flask
from config import DefaultConfig
from app.helpers import truncate, prepend_url


def create_app(config=None):
    app = Flask(__name__)
    with app.app_context():
        configure_app(app, config)
        configure_extensions(app)
        configure_blueprints(app)
        configure_jinja(app)
        configure_logging(app)
    return app


def configure_app(app, config=None):
    app.config.from_object(DefaultConfig)
    if config:
        app.config.from_object(config)


def configure_extensions(app):
    from app.extensions import db, login, migrate, mail, moment
    db.init_app(app)
    login.init_app(app)
    login.login_view = 'static_views.login'
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)


def configure_blueprints(app):
    from app.views import static_views
    from app.errors.views import errors
    from app.users.views import users
    for blueprint in [static_views, errors, users]:
        app.register_blueprint(blueprint)


def configure_jinja(app):
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    # Globals
    app.jinja_env.globals['APP_NAME'] = app.config['APP_NAME']

    # Filters
    app.jinja_env.filters['truncate'] = truncate
    app.jinja_env.filters['prepend_url'] = prepend_url


def configure_logging(app):
    if not app.debug and not app.testing:
        log_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../../logs'))
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        app_name = app.config.get('APP_NAME')
        file_handler = RotatingFileHandler(
            '{}/{}.log'.format(log_dir, app_name),
            maxBytes=10240, backupCount=10)
        format_string = ('%(asctime)s %(levelname)s: %(message)s '
                         '[in %(pathname)s:%(lineno)d]')
        file_handler.setFormatter(logging.Formatter(format_string))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('{} startup'.format(app_name))

        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], credentials=auth, secure=secure,
                subject='{} failure'.format(app.config['APP_NAME']))
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
