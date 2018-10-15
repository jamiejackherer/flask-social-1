"""
    app.users.models.notification
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Notifications model.
"""
import json
from sqlalchemy import or_
from datetime import datetime
from app.extensions import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    payload_json = db.Column(db.Text)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_data(self):
        return json.loads(str(self.payload_json))


class NotificationHelper:
    _payload = dict()
    _post = None
    _comment = None

    def __init__(self, notified=None, notifier=None, post=None, comment=None):
        if notified:
            self._payload['notified_id'] = notified.id
        if notifier:
            self._payload['notifier_id'] = notifier.id
        if post:
            self._payload['post_id'] = post.id
            self._post = post
        if comment:
            self._payload['comment_id'] = comment.id
            self._comment = comment

    def follow(self):
        self._payload['name'] = 'follow'
        self.add()

    def post(self):
        self._payload['name'] = 'post'
        self.add()

    def post_like(self):
        self._payload['name'] = 'post_like'
        post = self._post
        self.add()
        if post.author != post.recipient:
            self._payload.update({
                'name': 'post_like_wall',
                'notified_id': post.recipient.id
            })
            self.add()

    def comment(self):
        self._payload['name'] = 'comment'
        comment = self._comment
        self.add()
        if comment.post.author != comment.post.recipient:
            self._payload.update({
                'name': 'comment_wall',
                'notified_id': comment.post.recipient.id
            })
            self.add()

    def comment_like(self):
        self._payload['name'] = 'comment_like'
        comment = self._comment
        self.add()
        if comment.author != comment.post.author:
            self._payload.update({
                'name': 'comment_like_post',
                'notified_id': comment.post.author.id
            })
            self.add()
        if comment.post.author != comment.post.recipient and \
                comment.author != comment.post.recipient:
            self._payload.update({
                'name': 'comment_like_wall',
                'notified_id': comment.post.recipient.id
            })
            self.add()

    def delete_follow(self):
        s_name = '%"name": "follow"%'
        notification = Notification.query.filter(
            Notification.payload_json.like(s_name),
            Notification.user_id == self._payload.get('notified_id'))
        notification.delete(synchronize_session=False)

    def delete_post(self):
        s_post_id = '%"post_id": {}%'.format(self._payload.get('post_id'))
        notifications = Notification.query.filter(
            Notification.payload_json.like(s_post_id))
        notifications.delete(synchronize_session=False)

    def delete_post_like(self):
        post_id = self._payload.get('post_id')
        notifier_id = self._payload.get('notifier_id')
        s_post_id = '%"post_id": {}%'.format(post_id)
        s_notifier_id = '%"notifier_id": {}%'.format(notifier_id)
        s_post_like = '%"name": "post_like"%'
        s_post_like_wall = '%"name": "post_like_wall"%'
        notifications = Notification.query.filter(
            Notification.payload_json.like(s_post_id),
            Notification.payload_json.like(s_notifier_id),
            or_(Notification.payload_json.like(s_post_like),
                Notification.payload_json.like(s_post_like_wall)))
        notifications.delete(synchronize_session=False)

    def delete_comment(self):
        s_comment_id = '%"comment_id": {}%'.\
            format(self._payload.get('comment_id'))
        notifications = Notification.query.filter(
            Notification.payload_json.like(s_comment_id))
        notifications.delete(synchronize_session=False)

    def delete_comment_like(self):
        comment_id = self._payload.get('comment_id')
        notifier_id = self._payload.get('notifier_id')
        s_comment_id = '%"comment_id": {}%'.format(comment_id)
        s_notifier_id = '%"notifier_id": {}%'.format(notifier_id)
        s_comment_like = '%"name": "comment_like"%'
        s_comment_like_post = '%"name": "comment_like_post"%'
        s_comment_like_wall = '%"name": "comment_like_wall"%'
        notifications = Notification.query.filter(
            Notification.payload_json.like(s_comment_id),
            Notification.payload_json.like(s_notifier_id),
            or_(Notification.payload_json.like(s_comment_like),
                Notification.payload_json.like(s_comment_like_post),
                Notification.payload_json.like(s_comment_like_wall)))
        notifications.delete(synchronize_session=False)

    def delete_by_user(self):
        notifier_id = self._payload.get('notifier_id')
        s_notifier_id = '%"notifier_id": {}%'.format(notifier_id)
        notifications = Notification.query.filter(
            Notification.payload_json.like(s_notifier_id))
        notifications.delete(synchronize_session=False)

    def add(self):
        payload = self._payload
        if payload.get('notifier_id') == payload.get('notified_id'):
            return
        user_id = payload.get('notified_id')
        del payload['notified_id']
        n = Notification(user_id=user_id, payload_json=json.dumps(payload))
        db.session.add(n)
