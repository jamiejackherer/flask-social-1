"""
    social
    ~~~~~~

    Callable `app` instance.
"""
import os
import config
from app.app import create_app
from app.extensions import db
from app.users.models import User, Post
from testing.default_user_content import DefaultUserContent


if os.environ.get('FLASK_ENV') == 'production':
    app = create_app(config.ProductionConfig)
else:
    app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'app': app,
        'db': db,
        'User': User,
        'Post': Post,
        'DUC': DefaultUserContent,
        'p': Post.query.filter_by(id=2).first(),
    }
