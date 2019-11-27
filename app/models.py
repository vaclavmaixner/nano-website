from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_type = db.Column(db.String(64))
    heading = db.Column(db.String())
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Article {}>'.format(self.heading)


class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String())
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Grant {}>'.format(self.heading)


class Instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String())
    full_heading = db.Column(db.String())
    body = db.Column(db.Text())
    preview_text = db.Column(db.Text())
    footnote = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Instrument {}>'.format(self.heading)

class Thesis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String())
    body = db.Column(db.Text())
    preview_text = db.Column(db.Text())
    footnote = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Thesis {}>'.format(self.heading)



# class Human_group(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique = True)
#     # human_id = db.Column(db.Integer, db.ForeignKey('human.id'))
#     # humans = db.relationship('Human', backref='human_group', lazy='dynamic')
    
#     def __repr__(self):
#         return '<Human_group {}>'.format(self.name)

# group_choices = 
# {
#     'group': [
#         'group_leader', 'researcher'
#     ]
# }

class Human(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(), index=True)
    # group = db.relationship('Human_group', backref='human')
    # group = db.Column(db.String(), db.ForeignKey('human_group.id'))
    slug = db.Column(db.String(64), index=True, unique=True)
    full_name = db.Column(db.String(64), index=True, unique=True)
    full_name_cz = db.Column(db.String(64), index=True, unique=True)
    position = db.Column(db.String())
    email = db.Column(db.String(120), index=True, unique=True)
    telephone = db.Column(db.String(120))
    links = db.Column(db.String())
    ##ids = db.Column(db.String())
    orcid = db.Column(db.String(64))
    researcher_id = db.Column(db.String(64))
    scopus_id = db.Column(db.String())
    about_text = db.Column(db.Text())

    def __repr__(self):
        return '<Human {}>'.format(self.full_name)

class ImageView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/image.html')
        
class HumanView(ModelView):
    form_widget_args = {
        'about_text': {
            'rows': 15,
            'style': 'width: 800px'
        }
    }

class GrantView(ModelView):
    form_widget_args = {
        'body': {
            'rows': 20,
            'style': 'width: 800px'
        },
        'heading': {
            'style': 'width: 800px'
        }
    }

class InstrumentView(ModelView):
    form_widget_args = {
        'heading': {
            'style': 'width: 800px'
        },
        'full_heading': {
            'style': 'width: 800px'
        },
        'body': {
            'rows': 25,
            'style': 'width: 800px'
        },
        'preview_text': {
            'rows': 8,
            'style': 'width: 800px'
        },
        'footnote': {
            'style': 'width: 800px'
        },
        
    }

class ThesisView(ModelView):
    form_widget_args = {
        'heading': {
            'style': 'width: 800px'
        },
        'body': {
            'rows': 25,
            'style': 'width: 800px'
        },
        'preview_text': {
            'rows': 8,
            'style': 'width: 800px'
        },
        'footnote': {
            'style': 'width: 800px'
        },
        
    }