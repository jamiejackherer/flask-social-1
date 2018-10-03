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
from app.users.models.post import Post
from app.users.models.post_comment import PostComment


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
        'PostComment': PostComment,
        'p': Post.query.filter_by(id=5).first(),
    }
