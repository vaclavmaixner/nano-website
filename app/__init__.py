from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_googlemaps import GoogleMaps

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
GoogleMaps(app)

# app_admin = Admin(name='My admin name', template_mode='bootstrap3')
admin = Admin(app, name='Admin Zone')


from app import routes, models
