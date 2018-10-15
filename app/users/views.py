"""
    app.users.views
    ~~~~~~~~~~~~~~~

    Views for users.
"""
from datetime import datetime
from sqlalchemy import or_
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.users.models.user import User
from app.users.models.posts import (
    Post, PostLike, PostComment, PostCommentLike, PostEdit, PostCommentEdit
)
from app.users.models.notification import NotificationHelper
from app.users.forms import (
    PostForm, SettingsAccountForm, SettingsProfileForm, SettingsPasswordForm,
    SearchForm, SettingsMiscellaneousForm, SettingsDeleteAccountForm
)


users = Blueprint('users', __name__)


@users.before_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.active:
            return redirect(url_for('static_views.logout'))
        current_user.last_seen = datetime.utcnow()
        current_user.commit()


@users.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user,
                    recipient=current_user)
        post.commit()
        flash('Your post is now live!')
        return redirect(url_for('users.home'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.home_posts.\
        paginate(page, current_user.posts_per_page, False)
    unfollowed_posts = current_user.unfollowed_posts.limit(8).all()
    return render_template('users/home.html', form=form, posts=posts,
                           unfollowed_posts=unfollowed_posts,
                           user=current_user)


@users.route('/<username>/posts')
@login_required
def my_posts(username):
    user = User.query.filter_by(username=username, active=True).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.my_posts.\
        order_by(Post.created.desc()).\
        paginate(page, current_user.posts_per_page, False)
    unfollowed_posts = current_user.unfollowed_posts.limit(8).all()
    return render_template('users/my-posts.html', posts=posts, user=user,
                           unfollowed_posts=unfollowed_posts)


@users.route('/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    """ User's profile.

    :param username: username to show profile
    """
    user = User.query.filter_by(username=username, active=True).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user,
                    recipient=user)
        post = post.commit()
        NotificationHelper(notified=user, notifier=current_user,
                           post=post).post()
        post.commit()
        flash('Your post is now live!')
        return redirect(url_for('users.profile', username=username))
    page = request.args.get('page', 1, type=int)
    posts = user.profile_posts.\
        order_by(Post.created.desc()).\
        paginate(page, current_user.posts_per_page, False)
    return render_template('users/profile.html', user=user, posts=posts,
                           form=form)


@users.route('/<username>/followers', methods=['GET', 'POST'])
@login_required
def followers(username):
    """ Show who is following `username`.

    :param username: username of user to show followers
    """
    user = User.query.filter_by(username=username, active=True).first_or_404()
    page = request.args.get('page', 1, type=int)
    followers = user.get_followers.paginate(
        page, current_user.posts_per_page, False)
    return render_template('users/followers.html', user=user,
                           followers=followers)


@users.route('/<username>/following', methods=['GET', 'POST'])
@login_required
def following(username):
    """ Show who `username` is following.

    :param username: username of user to show following
    """
    user = User.query.filter_by(username=username, active=True).first_or_404()
    page = request.args.get('page', 1, type=int)
    following = user.get_followed.paginate(
        page, current_user.posts_per_page, False)
    return render_template('users/following.html', user=user,
                           following=following)


@users.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    recent_users = User.query.filter(
        User.active == True, # noqa
        User.id != current_user.id).order_by(
            User.last_seen.desc()).limit(10)
    searchable = '%{}%'.format(request.args.get('search'))
    page = request.args.get('page', 1, type=int)
    search_result = User.query.filter(or_(
        User.first_name.like(searchable),
        User.last_name.like(searchable),
        User.username.like(searchable),
        User.full_name.like(searchable),
        User.email.like(searchable)))
    search_result_count = search_result.count()
    search_result = search_result.paginate(
        page, current_user.posts_per_page, False)
    return render_template(
        'users/search.html', form=form, search_result=search_result,
        recent_users=recent_users, search_result_count=search_result_count)


@users.route('/<username>/<action>')
@login_required
def user_action(username, action):
    """ User actions.

    :param username: Username to take action upon
    :param action: Action to take on `username`
    """
    user = User.query.filter_by(username=username, active=True).first_or_404()
    # Do not allow users to take action on themselves.
    no_self_action = ['follow', 'unfollow']
    if action in no_self_action and user == current_user:
        return redirect(url_for('users.home'))
    # Follow user.
    if action == 'follow':
        current_user.follow(user)
        NotificationHelper(notified=user, notifier=current_user).follow()
        current_user.commit()
        flash('You are now following {}.'.format(user.full_name))
    # Unfollow user.
    if action == 'unfollow':
        current_user.unfollow(user)
        NotificationHelper(notified=user).delete_follow()
        current_user.commit()
        flash('You are no longer following {}.'.format(user.full_name))
    return redirect(request.referrer)


@users.route('/posts/post', methods=['GET', 'POST'])
@login_required
def post():
    post_id = request.args.get('post_id')
    posts = Post.post_by_id(post_id).first_or_404()

    comments_page = request.args.get('comments_page', 1, type=int)
    comments = posts.active_comments.order_by(
        PostComment.created.asc()).paginate(
            comments_page, current_user.posts_per_page, False)

    likes_page = request.args.get('likes_page', 1, type=int)
    likes = posts.active_likes.order_by(
        PostLike.created.desc()).paginate(
            likes_page, current_user.posts_per_page, False)

    form = PostForm()
    if form.validate_on_submit():
        post_comment = PostComment(body=form.body.data, author=current_user,
                                   post_id=post_id)
        comment = post_comment.commit()
        NotificationHelper(notified=comment.post.author,
                           notifier=current_user, comment=comment).comment()
        comment.commit()
        flash('Your post is now live!')
        return redirect(url_for('users.post', post_id=post_id))
    return render_template('users/post.html', posts=posts, form=form,
                           comments=comments, likes=likes)


@users.route('/posts/post-edit', methods=['GET', 'POST'])
@login_required
def post_edit():
    post_id = request.args.get('post_id')
    post = Post.post_by_id(post_id).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        # Check to make sure the post was actually edited, and that the
        # user is authorized to make edits on the post.
        if current_user == post.author and not form.body.data == post.body:
            old_post = post.body
            post.body = form.body.data
            post_edit = PostEdit(body=old_post, user_id=current_user.id,
                                 post_id=post.id, created=post.created)
            post.created = datetime.utcnow()
            db.session.add(post_edit)
            post.commit()
            flash('Your post has been updated.')
            return redirect(url_for('users.post_edit', post_id=post_id))
    elif request.method == 'GET':
        form.body.data = post.body
    return render_template('users/post-edit.html', post=post, form=form)


@users.route('/posts/comment')
@login_required
def comment():
    comment_id = request.args.get('comment_id')
    posts = PostComment.comment_by_id(comment_id).first_or_404()
    page = request.args.get('page', 1, type=int)
    likes = posts.active_likes.order_by(
        PostCommentLike.created.desc()).paginate(
            page, current_user.posts_per_page, False)
    return render_template('users/comment.html', posts=posts,
                           likes=likes)


@users.route('/posts/comment-edit', methods=['GET', 'POST'])
@login_required
def comment_edit():
    comment_id = request.args.get('comment_id')
    comment = PostComment.comment_by_id(comment_id).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        # Check to make sure the comment was actually edited, and that the
        # user is authorized to make edits on the comment.
        if (current_user == comment.author and
                not form.body.data == comment.body):
            old_comment = comment.body
            comment.body = form.body.data
            comment_edit = PostCommentEdit(
                body=old_comment, user_id=current_user.id,
                comment_id=comment.id, created=comment.created)
            comment.created = datetime.utcnow()
            db.session.add(comment_edit)
            comment.commit()
            flash('Your comment has been updated.')
            return redirect(url_for('users.comment_edit',
                                    comment_id=comment_id))
    elif request.method == 'GET':
        form.body.data = comment.body
    return render_template('users/comment-edit.html', post=comment,
                           form=form)


@users.route('/post-action/<int:post_id>/<action>')
@login_required
def post_action(post_id, action):
    """ Post actions.

    :param post_id: ID of the post to take action upon
    :param action: Action to take on post
    """
    referrer = request.referrer
    post = Post.query.filter_by(id=post_id).first_or_404()
    # Delete post.
    if action == 'delete':
        if current_user == post.author or current_user.id == post.recipient_id:
            referrer = url_for('users.home', username=current_user.username)
            post.delete()
            NotificationHelper(post=post).delete_post()
            post.commit()
            flash('Post was deleted.')
    # Like post.
    if action == 'like':
        current_user.like_post(post)
        NotificationHelper(notified=post.author, notifier=current_user,
                           post=post).post_like()
        current_user.commit()
    # Unlike post.
    if action == 'unlike':
        current_user.unlike_post(post)
        NotificationHelper(
            notifier=current_user,
            post=post).delete_post_like()
        current_user.commit()
    return redirect(referrer)


@users.route('/comment-action/<int:comment_id>/<action>')
@login_required
def comment_action(comment_id, action):
    """ Comment actions.

    :param comment_id: ID of the comment to take action upon
    :param action: Action to take on comment
    """
    referrer = request.referrer
    comment = PostComment.query.filter_by(id=comment_id).first_or_404()
    # Delete comment.
    if action == 'delete-comment':
        if current_user == comment.author:
            referrer = url_for('users.post', post_id=comment.post.id)
            comment.delete()
            NotificationHelper(comment=comment).delete_comment()
            comment.commit()
            flash('Comment was deleted.')
    # Like comment.
    if action == 'like-comment':
        current_user.like_comment(comment)
        NotificationHelper(notified=comment.author, notifier=current_user,
                           comment=comment, post=comment.post).comment_like()
        current_user.commit()
    # Unlike comment.
    if action == 'unlike-comment':
        current_user.unlike_comment(comment)

        NotificationHelper(notifier=current_user,
                           comment=comment).delete_comment_like()

        current_user.commit()
    return redirect(referrer)


@users.route('/notifications')
@login_required
def notifications():
    current_user.notification_last_read_time = datetime.utcnow()
    current_user.commit()
    notifications = current_user.get_notifications()
    return render_template('users/notifications.html',
                           notifications=notifications)


@users.route('/settings/account', methods=['GET', 'POST'])
@login_required
def settings_account():
    form = SettingsAccountForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.commit()
        flash('Your account settings have been updated.')
        return redirect(url_for('users.settings_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('users/settings/account.html', form=form)


@users.route('/settings/profile', methods=['GET', 'POST'])
@login_required
def settings_profile():
    form = SettingsProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.commit()
        flash('Your profile settings have been updated.')
        return redirect(url_for('users.settings_profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.bio.data = current_user.bio
        form.location.data = current_user.location
    return render_template('users/settings/profile.html', form=form)


@users.route('/settings/password', methods=['GET', 'POST'])
@login_required
def settings_password():
    form = SettingsPasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        current_user.commit()
        flash('Your password has been changed.')
        return redirect(url_for('users.settings_password'))
    return render_template('users/settings/password.html', form=form)


@users.route('/settings/miscellaneous', methods=['GET', 'POST'])
@login_required
def settings_miscellaneous():
    form = SettingsMiscellaneousForm()
    if form.validate_on_submit():
        current_user.posts_per_page = int(form.posts_per_page.data)
        current_user.commit()
        flash('Your settings have been updated.')
        return redirect(url_for('users.settings_miscellaneous'))
    elif request.method == 'GET':
        form.posts_per_page.default = str(current_user.posts_per_page)
        form.process()
    return render_template('users/settings/miscellaneous.html', form=form)


@users.route('/settings/delete-account', methods=['GET', 'POST'])
@login_required
def settings_delete_account():
    form = SettingsDeleteAccountForm()
    if form.validate_on_submit():
        current_user.delete()
        NotificationHelper(notifier=current_user).delete_by_user()
        current_user.commit()
        flash('Your account has been removed.')
        return redirect(url_for('users.home'))
    return render_template('users/settings/delete-account.html', form=form)
