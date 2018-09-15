from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'Swathi Sowmya',
        'title': 'Sentimental Analysis',
        'content': 'Sentiment Analysis is a common NLP task that Data Scientists need to perform. This is a straightforward guide to creating a barebones movie review classifier in Python. ' ,
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Sai Ram',
        'title': 'Overview of Flask',
        'content': 'Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. Wikipedia',
        'date_posted': 'April 21, 2018'
    }
]

posts1=[
    {
	    'author': 'Swathi Sowmya',
        'content': 'Date: 01.09.2018	The Mid-Semester Lab Test will be held on 11.09.2018 at 08:00 hrs. in CIC PC Lab-I. ' ,
        'date_posted': 'August 20, 2018'
	},
	{
	    
	    'author': 'Sai Ram',
        'content': 'Date: 12.07.2018	The First lab class will be held on 31.07.2018 at 08:00 hrs. in CIC PC Lab-I. ' ,
        'date_posted': 'June 19, 2018'
	},
	{
	    'author': 'Sai Ram',
        'content': 'Date: 30.07.2018	Create your account to Moodle Course Management Gystem. Get the instruction here.' ,
        'date_posted': 'May 19, 2018'
	}
]
	
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


	
@app.route("/about")
def about():
    return render_template('about.html', title='Authors')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/todo")
@login_required
def todo():
    return render_template('todo.html',title="To-Do")
	
@app.route("/announce")
@login_required
def announce():
    return render_template('announce.html',title="Announcements",posts=posts1)
	
@app.route("/labp")
@login_required
def labp():
    return render_template('labp.html',title="Lab Programs to work on")
	
	
@app.route("/progress")
@login_required
def progress():
    return render_template('progress.html',title="Progress Check")
	

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')