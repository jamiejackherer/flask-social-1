"""
    social
    ~~~~~~

    Callable `app` instance.
"""
import os
import config
from app.app import create_app
from app.extensions import db
from app.users.models import User, Post, PostComment
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
        'PostComment': PostComment,
        'p': Post.query.filter_by(id=5).first(),
        'c': PostComment.query.filter_by(id=1).first(),
    }
