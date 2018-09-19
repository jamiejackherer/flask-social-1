"""
    app.users.models.followers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Followers model.
"""
from datetime import datetime
from app.extensions import db


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('created', db.DateTime, default=datetime.utcnow, index=True)
)
