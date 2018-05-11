# Imports
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app
from Backend.SQLiteDatabase import Database
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    db = Database("Backend/swim_log.db")
    max_pace = db.get_max_pace()
    previous_entries = db.get_all_entries()
    return render_template('index.html', title='Home Page',
                           pace=max_pace, entries=previous_entries)#, posts=posts""")


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
        # Return user to page they tried to visit if not logged in, else go to index
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# Logout functionality
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
