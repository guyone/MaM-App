from flask_mail import Message
from app import app, mail
from flask import render_template, url_for
from app.token import generate_confirmation_token

def send_confirm_email(user):
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    msg = Message(
        '[Metal as Medicine] Confirm Your Email',
        recipients=[user.email],
        html=render_template('email/confirm_email.html', confirm_url=confirm_url),
        sender='noreply@metalasmedicine.com'
    )
    mail.send(msg)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('[Metal as Medicine] Password Reset Request', sender='noreply@metalasmedicine.com', recipients=[user.email])
    msg.html = render_template('email/reset_password.html', user=user, token=token)
    mail.send(msg)