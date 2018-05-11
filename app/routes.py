# Imports
from flask import render_template, flash, redirect, url_for
from app import app
from Backend.SQLiteDatabase import Database
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    db = Database("Backend/swim_log.db")
    max_pace = db.get_max_pace()
    previous_entries = db.get_all_entries()
    user = {'username': 'Tyler'}
    return render_template('index.html', title='Home', user=user,
                           pace=max_pace, entries=previous_entries)


# Login page flow
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to index page if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

# Logout functionality
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
