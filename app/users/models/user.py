"""
    app.users.models.user
    ~~~~~~~~~~~~~~~~~~~~~

    User model.
"""
import jwt
import json
from time import time
from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql.expression import and_
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
    bio = db.Column(db.Text)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts_per_page = db.Column(db.Integer, default=10, nullable=False)
    location = db.Column(db.String(255))
    admin = db.Column(db.Boolean, default=False)

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
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

    def __repr__(self):
        return '<User {} {} ({})>'.format(
            self.first_name, self.last_name, self.email)

    def set_default_username(self):
        self.username = hash_list([self.first_name, self.last_name,
                                  self.email])

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=monsterid&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    @property
    def unfollowed_users(self):
        return User.query.join(
            followers,
            and_(followers.c.followed_id == User.id,
                 followers.c.follower_id == self.id),
            isouter=True).filter(
                followers.c.follower_id == None, # noqa
                User.id != self.id,
                User.active == True) # noqa

    @property
    def unfollowed_posts(self):
        return Post.query.join(
            User, Post.author_id == User.id).join(
                followers,
                and_(followers.c.followed_id == User.id,
                     followers.c.follower_id == self.id),
                isouter=True).filter(
                    followers.c.follower_id == None, # noqa
                    User.id != self.id,
                    Post.author_id == Post.recipient_id,
                    User.active == True, # noqa
                    Post.active == True).order_by( # noqa
                        Post.created.desc())

    @property
    def get_followers(self):
        return self.followers.filter_by(active=True)

    @property
    def get_followed(self):
        return self.followed.filter_by(active=True)

    @property
    def followed_posts(self):
        """ Get posts where the author is the recipient, and posts
        that the user is following.
        """
        followed = Post.query.\
            join(User, User.id == Post.author_id).\
            join(followers, followers.c.followed_id == Post.author_id).filter(
                followers.c.follower_id == self.id,
                Post.author_id == Post.recipient_id,
                Post.active == True, # noqa
                User.active == True)

        return followed.union(self.profile_posts).order_by(Post.created.desc())

    @property
    def profile_posts(self):
        """ Get posts where the user is the recipient. """
        return Post.query.join(User, User.id == Post.author_id).filter(
            Post.recipient_id == self.id, User.active == True, # noqa
            Post.active == True)

    @property
    def my_posts(self):
        """ Get posts where the author is the recipient. """
        return Post.query.join(User, User.id == Post.recipient_id).filter(
            Post.recipient_id == self.id, User.active == True, # noqa
            Post.author_id == self.id, Post.active == True)

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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
