from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op

from flask_googlemaps import GoogleMaps


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
GoogleMaps(app)

from app import routes, models
# app_admin = Admin(name='My admin name', template_mode='bootstrap3')

from app.models import Article, Human, HumanView, User, Grant, GrantView
from app.models import Instrument, InstrumentView, Thesis, ThesisView, ImageView, HumanView


admin = Admin(app, name='Admin Zone')
admin.add_view(ModelView(Article, db.session))
admin.add_view(HumanView(Human, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(GrantView(Grant, db.session))
admin.add_view(InstrumentView(Instrument, db.session))
admin.add_view(ThesisView(Thesis, db.session))
admin.add_view(ImageView(name='Image', endpoint='image'))

path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
