"""
    app.users.models.notification
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Notifications model.
"""
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from app.extensions import db


class Notification:
    @classmethod
    def _post_notification(self, name, notifier_id, notified_id, post_id):
        if notifier_id != notified_id:
            n = PostNotification(
                name=name, notifier_id=notifier_id, notified_id=notified_id,
                post_id=post_id)
            db.session.add(n)

    @classmethod
    def post_notification(self, post):
        self._post_notification(
            'post', post.author_id, post.recipient_id,
            post.id)

    @classmethod
    def post_like_notification(self, current_user, post):
        self._post_notification(
            'post_like', current_user.id, post.author.id,
            post.id)
        if post.author.id != post.recipient.id:
            self._post_notification(
                'post_like_wall', current_user.id,
                post.recipient.id, post.id)

    @classmethod
    def delete_post_like_notification(self, current_user, post):
        n = PostNotification.query.filter_by(
            post_id=post.id, notifier_id=current_user.id).filter(or_(
                PostNotification.name == 'post_like',
                PostNotification.name == 'post_like_wall'))
        n.delete()

    @classmethod
    def _comment_notification(self, name, notifier_id, notified_id, post_id,
                              comment_id):
        if notifier_id != notified_id:
            n = CommentNotification(
                name=name, notifier_id=notifier_id, notified_id=notified_id,
                post_id=post_id, comment_id=comment_id)
            db.session.add(n)

    @classmethod
    def comment_notification(self, current_user, comment):
        self._comment_notification(
            'comment', current_user.id, comment.post.author.id,
            comment.post.id, comment.id)
        if comment.post.author.id != comment.post.recipient_id:
            self._comment_notification(
                'comment_wall', current_user.id,
                comment.post.recipient_id, comment.post_id, comment.id)

    @classmethod
    def comment_like_notification(self, current_user, comment):
        self._comment_notification(
            'comment_like', current_user.id, comment.author.id,
            comment.post.id, comment.id)
        if comment.author != comment.post.author:
            self._comment_notification(
                'comment_like_post', current_user.id, comment.post.author.id,
                comment.post.id, comment.id)

    @classmethod
    def delete_comment_like_notification(self, current_user, comment):
        n = CommentNotification.query.filter_by(
            comment_id=comment.id, notifier_id=current_user.id).filter(or_(
                CommentNotification.name == 'comment_like',
                CommentNotification.name == 'comment_like_post',
                CommentNotification.name == 'comment_like_wall'))
        n.delete()

    @classmethod
    def delete_comment_notification(self, comment):
        n = CommentNotification.query.filter_by(comment_id=comment.id)
        n.delete()

    @classmethod
    def delete_all_post_notifications(self, post):
        PostNotification.query.filter_by(post_id=post.id).delete()
        CommentNotification.query.filter_by(post_id=post.id).delete()


class NotificationMixin:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    read = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @declared_attr
    def notifier_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'))

    @declared_attr
    def notified_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'))


class PostNotification(db.Model, NotificationMixin):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<PostNotification {}>'.format(self.name)


class CommentNotification(db.Model, NotificationMixin):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('post_comment.id'))

    def __repr__(self):
        return '<CommentNotification {}>'.format(self.name)
