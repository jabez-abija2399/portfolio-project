from flask import Flask
from models import db, login_manager
from auth import auth
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a8476bd73b1e5123741e21f3642dec0e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db.init_app(app)

socketio = SocketIO(app)


login_manager.init_app(app)

# Register blueprints
app.register_blueprint(auth, url_prefix="/")

if __name__ == "__main__":
    with app.app_context():
        # Create all tables
        db.create_all()
    # app.run(host='0.0.0.0', port=5000, debug=True)
    socketio.run(app,debug=True)
