"""
    app.extensions
    ~~~~~~~~~~~~~~
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment


db = SQLAlchemy()
login = LoginManager()
migrate = Migrate() 
mail = Mail()
moment = Moment()
