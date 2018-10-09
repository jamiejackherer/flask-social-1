"""
    app.views
    ~~~~~~~~~

    Static views that do not require user login.
"""
from werkzeug.urls import url_parse
from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import func
from flask_login import current_user, login_user, logout_user
from app.forms import (
    LoginForm, RegisterForm, ResetPasswordRequestForm, ResetPasswordForm
)
from app.users.models.user import User
from app.helpers import register_user
from app.email import send_password_reset_email


static_views = Blueprint('static_views', __name__)


@static_views.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('users.feed'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = register_user(User, form.email.data, form.first_name.data,
                             form.last_name.data, form.password.data)
        login_user(user)
        return redirect(url_for('users.feed'))
    return render_template('index.html', form=form)


@static_views.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = register_user(User, form.email.data, form.first_name.data,
                             form.last_name.data, form.password.data)
        login_user(user)
        return redirect(url_for('users.feed'))
    return render_template('register.html', form=form)


@static_views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.feed'))
    form = LoginForm()
    if form.validate_on_submit():
        user_by_email = User.query.filter(
            func.lower(User.email) == func.lower(form.email.data)).first()
        user_by_username = User.query.filter(
            func.lower(User.username) == func.lower(form.email.data)).first()
        user = user_by_email if user_by_email else user_by_username
        if (user is None or not user.check_password(form.password.data) or not
                user.active):
            flash('Invalid email or password.')
            return redirect(url_for('static_views.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('static_views.index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@static_views.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('static_views.login'))


@static_views.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.feed'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('static_views.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.commit()
        flash('Your password has been reset.')
        return redirect(url_for('static_views.login'))
    return render_template('reset-password.html', form=form)


@static_views.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.feed'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for instructions.')
        return redirect(url_for('static_views.login'))
    return render_template('reset-password-request.html', form=form)
