# Imports
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from Backend.SQLiteDatabase import Database
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    db = Database("Backend/swim_log.db")
    max_pace = db.get_max_pace()
    previous_entries = db.get_all_entries()
    return render_template('index.html', title='Home Page',
                           pace=max_pace, entries=previous_entries)  # , posts=posts""")


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


# Registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect to index page if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# User Profile
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


# Edit Profile
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


# Function to track user's last time on the app
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
