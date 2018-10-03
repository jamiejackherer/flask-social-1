"""
    app.users.models.post
    ~~~~~~~~~~~~~~~~~~~~~

    Post model.
"""
from app.extensions import db
from app.models import BaseModel
from app.users.models.post_comment import PostComment


class Post(db.Model, BaseModel):
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    likes = db.relationship('PostLike', backref='post', lazy='dynamic')

    @property
    def t(self):
        pass

    def __repr__(self):
        return '<Post {}>'.format(self.body)
