"""
    app.users.models.post
    ~~~~~~~~~~~~~~~~~~~~~

    Post model.
"""
from datetime import datetime
from app.extensions import db
from app.models import BaseModel


class Post(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
