"""
initialize the eduWeb package
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_modals import Modal
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = '972c87379d16a8a27665666e1cf17a35c44d39d4feddceda9d600c4d8b304436'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eduweb.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
ckeditor = CKEditor(app)
modal = Modal(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS")
mail = Mail(app)
from eduWeb import routes