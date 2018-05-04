# Imports
from flask import render_template
from Frontend.app import app
from Backend.SQLiteDatabase import Database
from Frontend.app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    db = Database("Backend/swim_log.db")
    max_pace = db.get_max_pace()
    previous_entries = db.get_all_entries()
    user = {'username': 'Tyler'}
    return render_template('index.html', title='Home', user=user,
                           pace=max_pace, entries=previous_entries)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title ='Sign In', form=form)