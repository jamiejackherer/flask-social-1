"""
    app.users.models.post_likes
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Post likes model.
"""
from datetime import datetime
from app.extensions import db


class PostLikes(db.Model):
    __tablename__ = 'post_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
