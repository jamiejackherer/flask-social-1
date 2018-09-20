"""
    app.users.views
    ~~~~~~~~~~~~~~~

    Views for users.
"""
from datetime import datetime
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.users.models import User, Post
from app.users.forms import PostForm


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
        return redirect(url_for('users.home'))
    posts = current_user.followed_posts()
    return render_template('users/home.html', form=form, posts=posts)


@users.route('/list')
@login_required
def list():
    users = User.query.all()
    return render_template('users/list.html', users=users)


@users.route('/<username>/<action>')
@login_required
def user_action(username, action):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        return redirect(url_for('users.home'))
    full_name = user.get_full_name()

    # Follow user.
    if action == 'follow':
        current_user.follow(user)
        current_user.commit()

    # Unfollow user.
    if action == 'unfollow':
        current_user.unfollow(user)
        current_user.commit()

    return redirect(request.referrer)
