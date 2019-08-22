from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login


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
    body = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Article {}>'.format(self.body)

class Human(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    full_name = db.Column(db.String(64), index=True, unique=True)
    position = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    telephone = db.Column(db.String(120))
    links = db.Column(db.String(120))
    ids = db.Column(db.String())
    ##orcid = db.Column(db.String())
    ##researcher_id = db.Column(db.String())
    ##scopus_id = db.Column(db.String())

    def __repr__(self):
        return '<Human {}>'.format(self.full_name)