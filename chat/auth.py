from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user,LoginManager
from .models import db, User, Message
from .form import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from chat import socketio 
from flask_socketio import SocketIO,emit,send,join_room, leave_room



auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()
login_manager = LoginManager()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))

@auth.route('/')
@login_required
def home():
    return render_template('home.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.chat'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('auth.chat'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.chat'))
    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullName=form.FullName.data, username=form.username.data,
                    email=form.email.data, phoneNumber=form.phoneNumber.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
            
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('/chat')
@login_required
def chat():
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('chat.html', current_user=current_user, users=users)


@socketio.on('connect')
@login_required
def handle_connect():
    emit('private_chat_connected', {'room': current_user.id})


@socketio.on('join_private_chat')
@login_required
def handle_join_private_chat(data):
    other_user_id = int(data.get('other_user_id'))
    current_user_id = current_user.id
    room = f"{current_user_id}_{other_user_id}"
    join_room(room)
    emit('private_chat_started', {'room': room})

    # Retrieve previous messages between the sender and receiver
    messages = Message.query.filter(
        ((Message.sender_id == current_user_id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == current_user_id))
    ).all()

    # Prepare the previous messages to be sent to the client side
    previous_messages = []
    for message in messages:
        previous_messages.append({
            'content': message.content,
            'sender_id': User.query.get(message.sender_id).username,
            'receiver_id': User.query.get(message.receiver_id).username
        })

    emit('previous_private_messages', {'messages': previous_messages})


@socketio.on('send_private_message')
@login_required
def handle_send_private_message(data):
    other_user_id = int(data.get('other_user_id'))
    content = data.get('content')

    message = Message(sender_id=current_user.id, receiver_id=other_user_id, content=content)
    db.session.add(message)
    db.session.commit()

    room = f"{current_user.id}_{other_user_id}"

    # Emit the message to the receiver's room only
    emit('new_private_message', {'content': content, 'sender_id': current_user.username, 'receiver_id': User.query.get(other_user_id).username}, room=room)
