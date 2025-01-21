from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SECRET_KEY'] = 'secret!'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' # Redirect unauthorized users to the login page
login_manager.login_message_category = 'info'

from app import routes, models
