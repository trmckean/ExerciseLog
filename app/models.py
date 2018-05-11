from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


# Class representing database for users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # Function for user to set password (stores hash not pass)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Function to verify user password using hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # For convenient printing
    def __repr__(self):
        return '<User {}>'.format(self.username)


# Class representing table for posts by a user
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # For convenient printing
    def __repr__(self):
        return '<Post {}>'.format(self.body)
