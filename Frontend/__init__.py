from flask import Flask
from config import Config
from Frontend import test_flask

# Tell flask to read and apply config file
app = Flask(__name__)
app.config.from_object(Config)

