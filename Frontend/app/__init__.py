from flask import Flask
from Frontend.config import Config

# Tell flask to read and apply config file
app = Flask(__name__)
app.config.from_object(Config)

from Frontend.app import routes