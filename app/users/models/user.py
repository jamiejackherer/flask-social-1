"""
    app.users.models.user
    ~~~~~~~~~~~~~~~~~~~~~

    User model.
"""
import jwt
from time import time
from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import and_
from sqlalchemy.orm import column_property
from flask import current_app
from flask_login import UserMixin
from app.extensions import db, login
from app.models import BaseModel
from app.helpers import hash_list, AttrDict
# Import other models from bottom of file to avoid circular dependencies.


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
    notification_last_read_time = db.Column(db.DateTime)

    full_name = column_property(first_name + " " + last_name)
    followed = db.relationship(
        'User',
        secondary='followers',
        primaryjoin='followers.c.follower_id == User.id',
        secondaryjoin='followers.c.followed_id == User.id',
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic')
    post_author = db.relationship(
        'Post', foreign_keys='Post.author_id', backref='author',
        lazy='dynamic')
    post_recipient = db.relationship(
        'Post', foreign_keys='Post.recipient_id', backref='recipient',
        lazy='dynamic')
    post_likes = db.relationship(
        'PostLike', foreign_keys='PostLike.user_id', backref='user',
        lazy='dynamic')
    post_comments = db.relationship(
        'PostComment',
        foreign_keys='PostComment.author_id',
        backref='author', lazy='dynamic')
    post_comment_likes = db.relationship(
        'PostCommentLike',
        foreign_keys='PostCommentLike.user_id', backref='user',
        lazy='dynamic')
    notification = db.relationship(
        'Notification', order_by='desc(Notification.created)', lazy='dynamic')

    def __repr__(self):
        return '<User {} {} ({})>'.format(
            self.first_name, self.last_name, self.email)

    def set_default_username(self):
        """ Set `User`'s default username.

        Default usename is set by hashing FirstName_LastName_Email.

        See :mod:app.helpers :func:hash_list
        """
        self.username = hash_list([self.first_name, self.last_name,
                                  self.email])

    def set_password(self, password):
        """ Set `User` password.

        :param password: password string
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """ Check if `password` is euqal to `User.password`.

        :param password: password string
        """
        return check_password_hash(self.password, password)

    def avatar(self, size):
        """ Return avatar URL for `User` at the given `size`.

        :param size: integer for size of avatar to be returned
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=monsterid&s={}'.format(
            digest, size)

    def follow(self, user):
        """ Follow `user`.

        :param user: user model object of :class:User
        """
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """ Unfollow `user`.

        :param user: user model object of :class:User
        """
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """ Check if `User` is following `user`.

        :param user: user model object of :class:User
        """
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def like_post(self, post):
        """ Like `post`.

        :param post: post model object of :class:Post
        """
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        """ Like `post`.

        :param post: post model object of :class:Post
        """
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        """ Check if `User` has liked `post` or not.

        :param post: post model object of :class:Post
        """
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    def like_comment(self, comment):
        """ Like `comment`.

        :param comment: comment model object of :class:PostComment
        """
        if not self.has_liked_comment(comment):
            like = PostCommentLike(user_id=self.id, comment_id=comment.id)
            db.session.add(like)

    def unlike_comment(self, comment):
        """ Unlike `comment`.

        :param comment: comment model object of :class:PostComment
        """
        if self.has_liked_comment(comment):
            PostCommentLike.query.filter_by(
                user_id=self.id,
                comment_id=comment.id).delete()

    def has_liked_comment(self, comment):
        """ Check if `User` has liked `comment` or not.

        :param comment: comment model object of :class:PostComment
        """
        return PostCommentLike.query.filter(
            PostCommentLike.user_id == self.id,
            PostCommentLike.comment_id == comment.id).count() > 0

    @property
    def unfollowed_users(self):
        """ Return users `User` is not following. """
        return User.query.\
            join(followers,
                 and_(followers.c.followed_id == User.id,
                      followers.c.follower_id == self.id),
                 isouter=True).\
            filter(followers.c.follower_id == None,
                   User.id != self.id,
                   User.active == True).\
            limit(5) # noqa

    @property
    def home_posts(self):
        """ Return posts for `User`'s home feed.

        These are posts that `User` is following, and posts that `User` has
        posted on their own feed.
        """
        followed = Post.query.\
            join(User, User.id == Post.author_id).\
            join(followers, followers.c.followed_id == Post.author_id).\
            filter(followers.c.follower_id == self.id,
                   Post.author_id == Post.recipient_id,
                   Post.active == True, # noqa
                   User.active == True)
        return followed.union(self.profile_posts).order_by(Post.created.desc())

    @property
    def unfollowed_posts(self):
        """ Return posts that `User` is NOT following. """
        return Post.query.\
            join(User, Post.author_id == User.id).\
            join(followers,
                 and_(followers.c.followed_id == User.id,
                      followers.c.follower_id == self.id),
                isouter=True).\
            filter(followers.c.follower_id == None, # noqa
                   User.id != self.id,
                   Post.author_id == Post.recipient_id,
                   User.active == True, # noqa
                   Post.active == True).\
            order_by(Post.created.desc())

    @property
    def profile_posts(self):
        """ Get posts where `User` is the recipient. """
        return Post.query.join(User, User.id == Post.author_id).\
            filter(Post.recipient_id == self.id,
                   User.active == True, # noqa
                   Post.active == True)

    @property
    def my_posts(self):
        """ Get posts that `User` posted on their own feed. """
        return Post.query.join(User, User.id == Post.recipient_id).filter(
            Post.recipient_id == self.id, User.active == True, # noqa
            Post.author_id == self.id, Post.active == True)

    @property
    def get_followers(self):
        """ Return users that are following `User`. """
        return self.followers.filter_by(active=True)

    @property
    def get_followed(self):
        """ Return users `User` is following. """
        return self.followed.filter_by(active=True)

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

    def new_notifications(self):
        last_read_time = (
            self.notification_last_read_time or datetime(1900, 1, 1))
        return self.notification.filter(
            Notification.created > last_read_time).count()

    def get_notifications(self):
        result = []
        for n in self.notification:
            attrdict = AttrDict()
            # Set timestamp to ``attrdict``.
            attrdict.created = n.created
            # Loop through json payload and set attributes to ``attrdict``.
            data = n.get_data()
            for key, value in data.items():
                setattr(attrdict, key, value)

            if hasattr(attrdict, 'notifier_id'):
                notifier = User.query.filter_by(
                    id=attrdict.notifier_id).first()
                setattr(attrdict, 'notifier', notifier)

            needs_post = ['post_like', 'post_like_wall']
            if attrdict.name in needs_post:
                attrdict.post = Post.query.\
                    filter_by(id=attrdict.post_id).first()

            needs_comment = [
                'comment', 'comment_wall', 'comment_like',
                'comment_like_post', 'comment_like_wall'
            ]
            if attrdict.name in needs_comment:
                attrdict.comment = PostComment.query.\
                    filter_by(id=attrdict.comment_id).first()

            result.append(attrdict)
        return result


@login.user_loader
def load_user(id):
    """ Load `User` to `current_user`. For :mod:flask_login.

    :param id: ID of the `User` to load
    """
    return User.query.get(int(id))


# Import other models here to avoid circular dependencies.
from app.users.models.followers import followers # noqa
from app.users.models.posts import ( # noqa
    Post, PostLike, PostComment, PostCommentLike
)
from app.users.models.notification import Notification # noqa
