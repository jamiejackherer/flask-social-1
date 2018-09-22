from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, TextAreaField, PasswordField
)
from wtforms.validators import (
    ValidationError, DataRequired, Email, Length, EqualTo
)
from app.users.models.user import User


class PostForm(FlaskForm):
    body = TextAreaField('Say something', validators=[DataRequired()])
    submit = SubmitField('Post')


class SettingsAccount(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(max=35)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=255)])
    submit = SubmitField('Update')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(SettingsAccount, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email.')


class SettingsUserInfo(FlaskForm):
    first_name = StringField('First name',
                             validators=[DataRequired(), Length(max=35)])
    last_name = StringField('Last name',
                            validators=[DataRequired(), Length(max=35)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Update')


class SettingsPassword(FlaskForm):
    current_password = PasswordField(
        'Current password', validators=[DataRequired()])
    password = PasswordField(
        'New password',
        validators=[DataRequired(), Length(min=8, max=32)])
    password2 = PasswordField(
        'Repeat new password',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

    def validate_current_password(self, current_password):
        if not current_user.check_password(current_password.data):
            raise ValidationError('Incorrect password.')
