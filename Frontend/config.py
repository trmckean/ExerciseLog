import os

basedir = os.path.abspath(os.path.dirname(__file__))


# Class to hold configurations
class Config(object):
    # Flask-WTF uses secret key to protect from CSRF attacks
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Configuration for SQL Alchemy Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

