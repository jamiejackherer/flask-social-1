"""
    app.users.models.post_comment
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Post comment model.
"""
from app.extensions import db
from app.models import BaseModel


class PostComment(db.Model, BaseModel):
    body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
