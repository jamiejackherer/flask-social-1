"""
    app.users.views
    ~~~~~~~~~~~~~~~

    Views for users.
"""
from datetime import datetime
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.extensions import db
from app.users.models import User


users = Blueprint('users', __name__)


@users.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        current_user.commit()


@users.route('/home')
@login_required
def home():
    return render_template('users/home.html')
