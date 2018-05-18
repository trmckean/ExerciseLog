from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

# Association table representing followers of a user
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

# Class representing database for users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Many-to-many relationship of followers to followed
    followed = db.relationship(
        'User', secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id ==id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    # Function for user to set password (stores hash not pass)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Function to verify user password using hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # For convenient printing
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Function to return avatar for a given user based on email using gravatar service
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    # Function to return whether user is following another user
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # Function for user to follow another user
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    # Function for user to unfollow another user
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # Function to get posts from other followed users
    def followed_posts(self):
            # Query db for relevant posts from followed users
            followed_posts = Post.query.join(followers,
                                       (followers.c.followed_id == Post.user_id)).filter(
                    followers.c.follower_id == self.id)
            # Query db for own posts
            own_posts = Post.query.filter_by(user_id=self.id)
            # Return union of above queries in descending order
            return followed_posts.union(own_posts).order_by(Post.timestamp.desc())


# Class representing table for posts by a user
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # For convenient printing
    def __repr__(self):
        return '<Post {}>'.format(self.body)

# TODO: Class representing table for exercise log by a user


# User loader function for flask-login extension
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
