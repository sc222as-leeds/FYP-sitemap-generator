from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_admin import Admin
# from flask_login import LoginManager

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')
db = SQLAlchemy(app)
# login_manager = LoginManager()

# login_manager.init_app(app)

migrate = Migrate(app, db, render_as_batch=True)
# admin = Admin(app,template_mode='bootstrap4')

from app import views, models