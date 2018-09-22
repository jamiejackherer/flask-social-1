"""
    app.app
    ~~~~~~~

    Flask application factory.
"""
from flask import Flask
from config import DefaultConfig


def create_app(config=None):
    app = Flask(__name__)
    app.config['app'] = app
    with app.app_context():
        configure_app(app, config)
        configure_extensions(app)
        configure_blueprints(app)
        configure_jinja_globals(app)
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


def configure_jinja_globals(app):
    app.jinja_env.globals['APP_NAME'] = app.config['APP_NAME']
