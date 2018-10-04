"""
    app.users.models.followers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Followers model.
"""
import jwt
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
from app.helpers import hash_list


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('created', db.DateTime, default=datetime.utcnow)
)


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
    post_likes = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic')
    post_comments = db.relationship(
        'PostComment',
        foreign_keys='PostComment.author_id',
        backref='author', lazy='dynamic')
    post_comment_likes = db.relationship(
        'PostCommentLike',
        foreign_keys='PostCommentLike.user_id',
        backref='user', lazy='dynamic')

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

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    def like_comment(self, comment):
        if not self.has_liked_comment(comment):
            like = PostCommentLike(user_id=self.id, comment_id=comment.id)
            db.session.add(like)

    def unlike_comment(self, comment):
        if self.has_liked_comment(comment):
            PostCommentLike.query.filter_by(
                user_id=self.id,
                comment_id=comment.id).delete()

    def has_liked_comment(self, comment):
        return PostCommentLike.query.filter(
            PostCommentLike.user_id == self.id,
            PostCommentLike.comment_id == comment.id).count() > 0

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


class Post(db.Model, BaseModel):
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    comments = db.relationship('PostComment', backref='post', lazy='dynamic')

    @property
    def active_likes(self):
        """ Get active likes of post where:
            - The post containing the likes is active
            - The user that liked the post is active
        """
        return self.likes.\
            join(Post, Post.id == PostLike.post_id).\
            join(User, User.id == PostLike.user_id).filter(
                Post.active == True, # noqa
                User.active == True)

    @property
    def active_comments(self):
        """ Get active post comments where:
            - The post containing the comment is active
            - The post comment is active
            - The user who posted the comment is active
        """
        return self.comments.\
            join(Post, Post.id == PostComment.post_id).\
            join(User, User.id == PostComment.author_id).filter(
                Post.active == True, PostComment.active == True,
                User.active == True) # noqa

    @classmethod
    def post_by_id(self, post_id):
        """ Get post by ID where:
            - Post is active
            - User who posted the post is active

            :param post_id: ID of post to return
        """
        return self.query.\
            join(User, User.id == Post.author_id).filter(
                Post.active == True, # noqa
                User.active == True,
                Post.id == post_id)

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class PostComment(db.Model, BaseModel):
    body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    likes = db.relationship('PostCommentLike', backref='post_comment',
                            lazy='dynamic')

    @property
    def active_likes(self):
        return self.likes.\
            join(PostComment, PostComment.id == PostCommentLike.comment_id).\
            join(User, User.id == PostCommentLike.user_id).filter(
                PostComment.active == True, # noqa
                User.active == True)

    @classmethod
    def comment_by_id(self, comment_id):
        """ Get comment by ID where:
            - Comment is active
            - User who posted the comment is active

            :param comment_id: ID of comment to return
        """
        return self.query.\
            join(User, User.id == PostComment.author_id).filter(
                PostComment.active == True, # noqa
                User.active == True,
                PostComment.id == comment_id)

    def __repr__(self):
        return '<PostComment {}>'.format(self.body)


class PostCommentLike(db.Model):
    __tablename__ = 'post_comment_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('post_comment.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
