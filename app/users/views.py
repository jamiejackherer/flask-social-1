"""
    app.users.views
    ~~~~~~~~~~~~~~~

    Views for users.
"""
from datetime import datetime
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from app.users.models import User, Post
from app.users.forms import (
    PostForm, SettingsAccount, SettingsUserInfo, SettingsPassword
)


users = Blueprint('users', __name__)


@users.before_request
def before_request():
    if current_user.is_authenticated:
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
    posts = current_user.followed_posts().paginate(
        page, current_user.posts_per_page, False)
    return render_template('users/home.html', form=form, posts=posts)


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
    posts = user.post_recipient.filter(Post.active == 1).\
        order_by(Post.created.desc()).paginate(
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


@users.route('/list')
@login_required
def list():
    users = User.query.filter_by(active=True).all()
    return render_template('users/list.html', users=users)


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

    # Remove post.
    if action == 'delete-post':
        post_id = int(request.args.get('post_id'))
        post = Post.query.filter_by(id=post_id).first_or_404()
        if current_user == post.author or current_user.id == post.recipient_id:
            post.delete()
            post.commit()
            flash('Post was deleted.')

    return redirect(request.referrer)


@users.route('/settings/account', methods=['GET', 'POST'])
@login_required
def settings_account():
    form = SettingsAccount(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.commit()
        flash('Your settings have been updated.')
        return redirect(url_for('users.settings_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('users/settings/account.html', form=form)


@users.route('/settings/user-info', methods=['GET', 'POST'])
@login_required
def settings_user_info():
    form = SettingsUserInfo()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.about_me = form.about_me.data
        current_user.commit()
        flash('Your settings have been updated.')
        return redirect(url_for('users.settings_user_info'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.about_me.data = current_user.about_me
    return render_template('users/settings/user-info.html', form=form)


@users.route('/settings/password', methods=['GET', 'POST'])
@login_required
def settings_password():
    form = SettingsPassword()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        current_user.commit()
        flash('Your password has been changed.')
        return redirect(url_for('users.settings_password'))
    return render_template('users/settings/password.html', form=form)
