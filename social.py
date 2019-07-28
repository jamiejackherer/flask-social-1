"""
    social
    ~~~~~~

    uWSGI entry point.
"""
import os
import config
from app.app_factory import create_app
from app.extensions import db
from app.users.models.user import User
from app.users.models.posts import Post, PostComment
from app.users.models.notification import Notification
from app.fake_content import FakeContent


if os.environ.get('FLASK_ENV') == 'production':
    app = create_app(config.ProductionConfig)
else:
    app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'app': app,
            'db': db,
            'FC': FakeContent,
            'User': User,
            'Post': Post,
            'PostComment': PostComment,
            'Notification': Notification}
