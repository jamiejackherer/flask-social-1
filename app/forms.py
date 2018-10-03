"""
    app.forms
    ~~~~~~~~~
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField, BooleanField, PasswordField, SubmitField
)
from wtforms.validators import (
    ValidationError, DataRequired, Email, Length, EqualTo
)
from app.users.models import User


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
                                  'registered.'.format(email.data))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8, max=32)])
    password2 = PasswordField(
        'Repeat new password', validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('submit')
