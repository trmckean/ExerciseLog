# Imports
from flask import Flask
from flask import render_template
from Backend.SQLiteDatabase import Database
from Frontend.forms import LoginForm

app = Flask(__name__)


@app.route("/")
def hello():
    db = Database("../Backend/swim_log.db")
    max_pace = db.get_max_pace()
    previous_entries = db.get_all_entries()
    user = {'username': 'Tyler'}
    return render_template('index.html', title='Home', user=user,
                           pace=max_pace, entries=previous_entries)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title ='Sign In', form=form)

if __name__ == "__main__":
    app.run()
