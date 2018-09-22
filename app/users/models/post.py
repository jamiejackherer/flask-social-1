"""
    app.users.models.post
    ~~~~~~~~~~~~~~~~~~~~~

    Post model.
"""
from app.extensions import db
from app.models import BaseModel


class Post(db.Model, BaseModel):
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
