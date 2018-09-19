"""
    app.users.models.user
    ~~~~~~~~~~~~~~~~~~~~~

    User model.
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login
from app.models import BaseModel
from app.users.models.followers import followers
from app.helpers import hash_list


class User(UserMixin, db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(35), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    about_me = db.Column(db.Text)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic')

    def set_default_username(self):
        self.username = hash_list([self.first_name, self.last_name,
                                  self.email])

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def __repr__(self):
        return '<User {} {} ({})>'.format(
            self.first_name, self.last_name, self.email)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
