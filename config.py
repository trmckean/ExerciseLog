import os

# Class to hold configurations
class Config(object):
    #Flask-WTF uses secret key to protect from CSRF attacks
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
