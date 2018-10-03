"""
    app.users.views
    ~~~~~~~~~~~~~~~

    Views for users.
"""
from datetime import datetime
from sqlalchemy import or_
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from app.users.models import User, Post, PostLike
from app.users.forms import (
    PostForm, SettingsAccountForm, SettingsProfileForm, SettingsPasswordForm,
    SearchForm
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
    posts = current_user.followed_posts.paginate(
        page, current_user.posts_per_page, False)
    unfollowed_posts = current_user.unfollowed_posts.limit(8).all()
    return render_template('users/home.html', form=form, posts=posts,
                           unfollowed_posts=unfollowed_posts)


@users.route('/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username, active=True).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user,
                    recipient=user)
        post.commit()
        flash('Your post is now live!')
        return redirect(url_for('users.profile', username=username))
    page = request.args.get('page', 1, type=int)
    posts = user.profile_posts.order_by(
        Post.created.desc()).paginate(
            page, current_user.posts_per_page, False)
    return render_template('users/profile.html', user=user, posts=posts,
                           form=form)


@users.route('/<username>/followers', methods=['GET', 'POST'])
@login_required
def followers(username):
    user = User.query.filter_by(username=username, active=True).first_or_404()
    page = request.args.get('page', 1, type=int)
    followers = user.get_followers.paginate(
        page, current_user.posts_per_page, False)
    return render_template('users/followers.html', user=user,
                           followers=followers)


@users.route('/<username>/following', methods=['GET', 'POST'])
@login_required
def following(username):
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
    user = User.query.filter_by(username=username, active=True).first_or_404()

    # Do not allow users to take action on themselves.
    no_self_action = ['follow', 'unfollow']
    if action in no_self_action and user == current_user:
        return redirect(url_for('users.home'))

    # Follow user.
    if action == 'follow':
        current_user.follow(user)
        current_user.commit()
        flash('You are now following {}.'.format(user.full_name))

    # Unfollow user.
    if action == 'unfollow':
        current_user.unfollow(user)
        current_user.commit()
        flash('You are no longer following {}.'.format(user.full_name))

    return redirect(request.referrer)


@users.route('/<username>/posts/post-likes/<int:post_id>')
@login_required
def post_likes(username, post_id):
    user = User.query.filter_by(username=username, active=True).first_or_404()
    posts = Post.query.filter_by(
        id=post_id, author=user, active=True).first_or_404()
    likes = posts.likes.order_by(PostLike.created.desc()).all()
    return render_template('users/post-likes.html', user=user, likes=likes,
                           posts=posts)


@users.route('/<username>/posts/post-comments/<int:post_id>')
@login_required
def post_comments(username, post_id):
    user = User.query.filter_by(username=username, active=True).first_or_404()
    posts = Post.query.filter_by(
        id=post_id, author=user, active=True).first_or_404()

    return render_template('users/post-comments.html', user=user, posts=posts)


@users.route('/post-action/<int:post_id>/<action>')
@login_required
def post_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()

    if action == 'delete':
        if current_user == post.author or current_user.id == post.recipient_id:
            post.delete()
            post.commit()
            flash('Post was deleted')

    if action == 'like':
        current_user.like_post(post)
        current_user.commit()

    if action == 'unlike':
        current_user.unlike_post(post)
        current_user.commit()

    return redirect(request.referrer)


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
