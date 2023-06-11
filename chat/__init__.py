from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO,emit,send,join_room, leave_room
from .models import db,User
# from .auth import socketio

 

login_manager = LoginManager()
socketio = SocketIO()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a8476bd73b1e5123741e21f3642dec0e'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    from chat.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
