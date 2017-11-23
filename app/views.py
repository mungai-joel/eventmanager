"""modules and packages to be imported"""
from flask import request, redirect, render_template, url_for, flash, session
from wtforms import Form, StringField, PasswordField, TextField, validators
from functools import  wraps
from app import app
from .main.user import User

users = []


# app = Flask(__name__)

class RegisterForm(Form):
    """ create form input fields for register"""
    username = StringField('Username', 
                            [validators.Length(min=1, max=50)])
    email = TextField('Email',
                         [validators.DataRequired(),
                          validators.Email()])
    password = PasswordField('password', [
        validators.DataRequired(),
         validators.EqualTo('confirm',
                             message='password do not match'),
                              validators.Length(min=6, max=25)])
    confirm = PasswordField('confirm password')

@app.route('/')
@app.route('/index')
def index():
    """renders the index page"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """register users information"""
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        user = User(form.username.data, 
                    form.email.data,
                    form.password.data
                    )
        users.append(user)
        return redirect(url_for('create_bucketlist'))
    return render_template('register.html', form=form)

class LoginForm(Form):
    """create from input field for login"""
    email = TextField('Email address', [
        validators.DataRequired(), validators.Email()])
    password = PasswordField('password',
                             [validators.DataRequired()
                            ])

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login')
            return redirect(url_for('login', next=request.url))
    return decorated_function

@app.route('/login', methods=['GET','POST'])
def login():
    """verifies and login user """
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        for user in users:
            if user.email == form.email.data and\
             user.password == form.password.data:
                session['logged_in'] = user.email
                return redirect(url_for('create_bucketlist'))
            else:
                flash("Invalid credentials")
    return render_template('login.html', form=form)

class CreateBucketlist(Form):
    """create form input for bucketlist"""
    title = StringField('Title', [validators.DataRequired()])
    description = StringField('Description')

@app.route('/create_bucketlist', methods=['GET', 'POST'])
@login_required
def create_bucketlist():
    """renders the createbl page"""
    if not session['logged_in']:
        return redirect(url_for('login'))
    form = CreateBucketlist(request.form)
    if request.method == 'POST' and form.validate():
        for user in users:
            if user.email == session['logged_in']:
                user.create_bucketlist(form.title.data,
                                       form.description.data
                                       )
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'))
    return render_template('create_bucketlist.html', form=form)

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """renders dashboard dashboard html"""
    for user in users:
        if user.email == session['logged_in']:
            bucketlists = user.bucketlists
            return render_template('dashboard.html', 
                                    bucketlists=bucketlists
                                    )
    return redirect(url_for('login'))

@app.route('/delete_bucketlist/<id>', methods=['GET', 'POST'])
@login_required
def delete_bucketlist(id):
    """removes bucketlist that matches id passed"""
    for user in users:
        if user.email == session['logged_in']:
            user.delete_bucketlist(id)
            return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

class EditBucketlist(Form):
    """create form input fields for edit"""
    title = StringField('new title' , [validators.DataRequired()])
    description = StringField('new description', [validators.DataRequired()])

@app.route('/edit_bucketlist/<id>', methods=['GET', 'POST'])
@login_required
def edit_bucketlist(id):
    """edit user bucketlist"""
    form = EditBucketlist(request.form)
    if request.method == 'POST' and form.validate():
        for user in users:
            message= None
            if user.email == session['logged_in']:
                user.update_bucketlist(id, 
                    form.title.data, 
                    form.description.data 
                    )
                flash("Successfully Edited")
                return redirect(url_for('dashboard'))
    return render_template('edit_bucketlist.html', form=form)

class AddActivity(Form):
    """creates form input field for adding activity"""
    activity = StringField('Activity', [validators.DataRequired()])

@app.route('/add_activity/<id>', methods=['GET', 'POST'])
@login_required
def add_activity(id):
    """Add activity to bucketlist that matches id passed"""
    form = AddActivity(request.form)
    if request.method == 'POST' and form.validate():
        for user in users:
            if user.email == session['logged_in']:
                for v in user.bucketlists.values():
                    if id == v.id:
                        v.add_activity(form.activity.data)
                return redirect(url_for('activity_dashboard'))
    return render_template('add_activity.html', form=form)

@app.route('/activity_dashboard', methods=['GET', 'POST'])
@login_required
def activity_dashboard():
    """display activity of bucketlist"""
    if not session['logged_in']:
        return redirect(url_for('login'))
    for user in users:
        if user.email == session['logged_in']:
            bucketlists = user.bucketlists
            return render_template('activity_dashboard.html',
                                     bucketlists=bucketlists
                                    )
    return redirect(url_for('login'))

class EditActivity(Form):
    """create form input fields for edit"""
    new_activity = StringField('New Activity', [validators.DataRequired()])

@app.route('/edit_activity/<bucketlist_id>/<id>', methods=['GET', 'POST'])
@login_required
def edit_activity(bucketlist_id, id):
    """edit activity from bucketlist that matches id passes"""
    form = EditActivity(request.form)
    if request.method == "POST" and form.validate():
        for user in users:
            if session['logged_in']:
                user.bucketlists[bucketlist_id].edit_activity(id,
                                                    form.new_activity.data)
                return redirect(url_for('activity_dashboard'))
    return render_template('edit_activity.html', form=form)
    

@app.route('/delete_activity/<bucketlist_id>/<id>', methods=['GET', 'POST'])
@login_required
def delete_activity(bucketlist_id, id):
    """delete an activity that matches id passed"""
    for user in users:
        if user.email == session['logged_in']:
            user.bucketlists[bucketlist_id].delete_activity(id)   
            return redirect(url_for('activity_dashboard'))
    return redirect(url_for('login'))
    

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """remove user email session """
    session.clear()
    return redirect(url_for('login'))



