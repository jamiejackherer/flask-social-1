"""
    social
    ~~~~~~

    Callable `app` instance.
"""
import os
import config
from app.app import create_app
from app.extensions import db
from app.users.models.user import User
from app.users.models.posts import Post, PostComment
from app.users.models.notifications import (
    Notification, PostNotification, CommentNotification, AbstractNotification
)
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
        'DUC': DefaultUserContent,
        'User': User,
        'Post': Post,
        'PostComment': PostComment,
        'Notification': Notification,
        'PostNotification': PostNotification,
        'CommentNotification': CommentNotification,
        'AbstractNotification': AbstractNotification,
    }
