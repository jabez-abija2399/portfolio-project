from flask import Blueprint, render_template, request, flash, redirect, url_for
from form import RegistrationForm, LoginForm,Send_message
from flask_bcrypt import Bcrypt
from models import User, db
from flask_login import login_user, current_user, LoginManager, login_required
from flask_socketio import SocketIO,send, emit, join_room, leave_room


bcrypt = Bcrypt()



auth = Blueprint('auth', __name__)
login_manager = LoginManager()



socketio = SocketIO()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/')
def home():
    return render_template('home.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('auth.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullName=form.FullName.data, username=form.username.data,
                    email=form.email.data, phoneNumber=form.phoneNumber.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
            
        return redirect(url_for('auth.home'))
    return render_template('register.html', title='Register', form=form)


@auth.route('/index')
def index():
    return render_template('chat.html')



@auth.route('/users')
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    socketio.emit('user_list', {'users': user_list}, namespace='/')
    return {'users': user_list}


@socketio.on('connect')
def handle_connect():
    emit('connected', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('join_room', {'room': room})

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    emit('leave_room', {'room': room})

@socketio.on('message')
def handle_message(data):
    sender = data['sender']
    receiver = data['receiver']
    message = data['message']

    # Save the message to the database
    msg = Message(sender=sender, receiver=receiver, message=message)
    db.session.add(msg)
    db.session.commit()

    # Emit the message to the receiver
    emit('message', {'sender': sender, 'message': message}, room=receiver)
