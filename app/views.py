"""
    app.views
    ~~~~~~~~~

    Static views that do not require a user login.
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import func
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegisterForm
from app.users.models import User


static_views = Blueprint('static_views', __name__)


@static_views.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data)
        user.register()
        login_user(user)
        return redirect(url_for('users.home'))
    return render_template('index.html', form=form)


@static_views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user_by_email = User.query.filter(
            func.lower(User.email) == func.lower(form.email.data)).first()
        user_by_username = User.query.filter(
            func.lower(User.username) == func.lower(form.email.data)).first()
        user = user_by_email if user_by_email else user_by_username
        if user is None or not user.check_password(form.password.data):
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
