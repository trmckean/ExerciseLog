from flask import Flask
from config import Config
from Frontend import test_flask

app = Flask(__name__)
app.config.from_object(Config)

