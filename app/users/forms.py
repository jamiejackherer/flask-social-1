from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import (
    ValidationError, DataRequired, Email, Length, EqualTo
)


class PostForm(FlaskForm):
    body = TextAreaField('Say something', validators=[DataRequired()])
    submit = SubmitField('Post')
