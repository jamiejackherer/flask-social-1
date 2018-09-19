"""
    app.forms
    ~~~~~~~~~
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField, BooleanField, PasswordField, SubmitField, TextAreaField
)
from wtforms.validators import (
    ValidationError, DataRequired, Email, Length, EqualTo
)
from app.users.models.user import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    first_name = StringField('First name',
                             validators=[DataRequired(), Length(max=35)])
    last_name = StringField('Last name',
                            validators=[DataRequired(), Length(max=35)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8, max=32)])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('{} is already '
                                  'registered'.format(email.data))
