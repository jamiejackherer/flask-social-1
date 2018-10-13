"""
    app.users.models.notification
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Notifications model.
"""
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declared_attr, AbstractConcreteBase
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
        # If a user posts on their own wall, don't notify them twice
        # when someone likes their post.
        if post.author != post.recipient:
            self._post_notification(
                'post_like_wall', current_user.id, post.recipient.id,
                post.id)

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
        if comment.post.author != comment.post.recipient:
            self._comment_notification(
                'comment_wall', current_user.id, comment.post.recipient.id,
                comment.post.id, comment.id)

    @classmethod
    def comment_like_notification(self, current_user, comment):
        self._comment_notification(
            'comment_like', current_user.id, comment.author.id,
            comment.post.id, comment.id)
        if comment.author != comment.post.author:
            self._comment_notification(
                'comment_like_post', current_user.id, comment.post.author.id,
                comment.post.id, comment.id)
        if comment.post.author != comment.post.recipient and \
                comment.author != comment.post.recipient:
            self._comment_notification(
                'comment_like_wall', current_user.id,
                comment.post.recipient.id, comment.post.id, comment.id)

    @classmethod
    def follow_notification(self, current_user, user):
        n = FollowNotification(
            name='follow', notifier_id=current_user.id, notified_id=user.id)
        db.session.add(n)

    @classmethod
    def delete_follow_notification(self, current_user, user):
        n = FollowNotification.query.filter_by(
            notifier_id=current_user.id, notified_id=user.id)
        n.delete()

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


class AbstractNotification(AbstractConcreteBase, db.Model):
    __table__ = None


class NotificationBaseModel:
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

    def __repr__(self):
        return '<PostNotification {}>'.format(self.name)


class PostNotification(AbstractNotification, NotificationBaseModel):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_id = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'post_notification',
        'concrete': True
        }


class CommentNotification(AbstractNotification, NotificationBaseModel):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('post_comment.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'comment_notification',
        'concrete': True
        }


class FollowNotification(AbstractNotification, NotificationBaseModel):
    __mapper_args__ = {
        'polymorphic_identity': 'follow_notification',
        'concrete': True
        }
