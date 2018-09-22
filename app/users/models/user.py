"""
    app.users.models.user
    ~~~~~~~~~~~~~~~~~~~~~

    User model.
"""
from time import time
from datetime import datetime
from hashlib import md5
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import column_property
from flask import current_app
from flask_login import UserMixin
from app.extensions import db, login
from app.models import BaseModel
from app.users.models.post import Post
from app.users.models.followers import followers
from app.helpers import hash_list


class User(UserMixin, db.Model, BaseModel):
    username = db.Column(db.String(35), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    about_me = db.Column(db.Text)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts_per_page = db.Column(db.Integer, default=10, nullable=False)

    full_name = column_property(first_name + " " + last_name)
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin='followers.c.follower_id == User.id',
        secondaryjoin='followers.c.followed_id == User.id',
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic')
    post_author = db.relationship(
        'Post',
        foreign_keys='Post.author_id',
        backref='author', lazy='dynamic')
    post_recipient = db.relationship(
        'Post',
        foreign_keys='Post.recipient_id',
        backref='recipient', lazy='dynamic')

    def set_default_username(self):
        self.username = hash_list([self.first_name, self.last_name,
                                  self.email])

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers,
            (followers.c.followed_id == Post.author_id)).filter(
                followers.c.follower_id == self.id,
                Post.author_id == Post.recipient_id,
                'Post.active == True')
        my_posts = Post.query.filter_by(recipient_id=self.id, active=True)
        return followed.union(my_posts).order_by(Post.created.desc())

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires},
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return User.query.get(id)

    def testing(self):
        return current_app

    def __repr__(self):
        return '<User {} {} ({})>'.format(
            self.first_name, self.last_name, self.email)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
