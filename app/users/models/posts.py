from datetime import datetime
from app.extensions import db
from app.models import BaseModel
# Import other models from bottom of file to avoid circular dependencies.


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


from app.users.models.user import User # noqa
