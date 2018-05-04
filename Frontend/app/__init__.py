from flask import Flask
from Frontend.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Tell flask to read and apply config file
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from Frontend.app import routes, models