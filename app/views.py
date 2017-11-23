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
    return render_template('events.html')

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
        return redirect(url_for('create_events'))
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
                return redirect(url_for('create_events'))
            else:
                flash("Invalid credentials")
    return render_template('login.html', form=form)

class CreateEvent(Form):
    """create form input for events"""
    title = StringField('Title', [validators.DataRequired()])
    description = StringField('Description')
    categpry = StringField('Category', [validators.DataRequired()])
    location = StringField('Location', [validators.DataRequired()])



@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    """renders the createbl page"""
    if not session['logged_in']:
        return redirect(url_for('login'))
    form = CreateEvent(request.form)
    if request.method == 'POST' and form.validate():
        for user in users:
            if user.email == session['logged_in']:
                user.create_event(form.title.data,
                                       form.description.data
                                       )
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'))
    return render_template('create_event.html', form=form)



@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """renders dashboard dashboard html"""
    for user in users:
        if user.email == session['logged_in']:
            events = user.events
            return render_template('dashboard.html', 
                                    events=events
                                    )
    return redirect(url_for('login'))


@app.route('/delete_event/<id>', methods=['GET', 'POST'])
@login_required
def delete_event(id):
    """removes events that matches id passed"""
    for user in users:
        if user.email == session['logged_in']:
            user.delete_event(id)
            return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


class EditEvent(Form):
    """create form input fields for edit"""
    title = StringField('new title' , [validators.DataRequired()])
    description = StringField('new description', [validators.DataRequired()])
    category = StringField('new category', [validators.DataRequired()])
    location = StringField('new location', [validators.DataRequired()])

@app.route('/edit_events/<id>', methods=['GET', 'POST'])
@login_required
def edit_events(id):
    """edit user events"""
    form = EditEvent(request.form)
    if request.method == 'POST' and form.validate():
        for user in users:
            message= None
            if user.email == session['logged_in']:
                user.update_event(id, 
                    form.title.data, 
                    form.description.data, 
                    form.category.data,
                    form.location.data,
                    )
                flash("Successfully Edited")
                return redirect(url_for('dashboard'))
    return render_template('edit_event.html', form=form)


class AddReservation(Form):
    """creates form input field for adding reservation"""
    name = StringField('Name', [validators.DataRequired()])
    phone = StringField('Phone')

@app.route('/add_reservation/<id>', methods=['GET', 'POST'])
@login_required
def add_reservation(id):
    """Add reservation to events that matches id passed"""
    form = AddReservation(request.form)
    if request.method == 'POST' and form.validate():
        for user in users:
            if user.email == session['logged_in']:
                for v in user.events.values():
                    if id == v.id:
                        v.add_reservation(form.activity.data)
                return redirect(url_for('activity_dashboard'))
    return render_template('add_reservation.html', form=form)


@app.route('/reservation_dashboard', methods=['GET', 'POST'])
@login_required
def reservation_dashboard():
    """display reservations of events"""
    if not session['logged_in']:
        return redirect(url_for('login'))
    for user in users:
        if user.email == session['logged_in']:
            events = user.events
            return render_template('reservations_dashboard.html',
                                     events=events
                                    )
    return redirect(url_for('login'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """remove user email session """
    session.clear()
    return redirect(url_for('login'))



