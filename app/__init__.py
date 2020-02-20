import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment

app                                     = Flask(__name__)
app.config['SECRET_KEY']                = '74b4b60118c0a6f801e7f4465a0fabef'
app.config['SQLALCHEMY_DATABASE_URI']   = 'sqlite:///site.db'
# app.config['SQLALCHEMY_DATABASE_URI']   = 'sqlite:///site.db'
app.config['SECURITY_PASSWORD_SALT']    = 'randomnumbersarethebest'
db              = SQLAlchemy(app)
bcrypt          = Bcrypt(app)
login_manager   = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'mail.metalasmedicine.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'noreply@metalasmedicine.com'
app.config['MAIL_PASSWORD'] = 'Metal4Metal2020!'
mail = Mail(app)

moment = Moment(app)

from app import routes