import re
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


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')


class SettingsAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(max=35)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=255)])
    submit = SubmitField('Update Account')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(SettingsAccountForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        # Make sure ``username``:
        # - Has alphanumeric / underscore
        # - Starts with alpha
        # - Doesn't start or end with an underscore
        regex = '^[a-zA-Z][a-zA-Z1-9_]*[a-zA-Z0-9]+$'
        if not re.match(regex, username.data):
            raise ValidationError('Invalid username. Example: john_doe13')

        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email.')


class SettingsProfileForm(FlaskForm):
    first_name = StringField('First name',
                             validators=[DataRequired(), Length(max=35)])
    last_name = StringField('Last name',
                            validators=[DataRequired(), Length(max=35)])
    bio = TextAreaField('Bio')
    location = StringField('Location', validators=[Length(max=255)])
    submit = SubmitField('Update Profile')


class SettingsPasswordForm(FlaskForm):
    current_password = PasswordField(
        'Old password', validators=[DataRequired()])
    password = PasswordField(
        'New password',
        validators=[DataRequired(), Length(min=8, max=32)])
    password2 = PasswordField(
        'Confirm new password',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update Password')

    def validate_current_password(self, current_password):
        if not current_user.check_password(current_password.data):
            raise ValidationError('Incorrect password.')


class SettingsDeleteAccountForm(FlaskForm):
    username = StringField(
        'Verify your username', validators=[DataRequired()])
    password = PasswordField(
        'Confirm your password', validators=[DataRequired()])
    submit = SubmitField('Delete Account')

    def validate_username(self, username):
        if current_user.username != username.data:
            raise ValidationError(
                'Incorrect username. Make sure you type your username '
                'exactly as it is.')

    def validate_password(self, password):
        if not current_user.check_password(password.data):
            raise ValidationError('Incorrect password.')
