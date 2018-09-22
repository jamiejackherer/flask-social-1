"""
    app.email
    ~~~~~~~~~
"""
from threading import Thread
from flask import render_template, current_app
from flask_mail import Message
from app.extensions import mail


def send_async_email(current_app, msg):
    with current_app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('Reset password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('/email/reset-password.txt',
                                         user=user, token=token),
               html_body=render_template('/email/reset-password.html',
                                         user=user, token=token))
