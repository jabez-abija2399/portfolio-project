from chat import create_app
from chat.auth import socketio
from chat.models import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        db.session.commit()
    socketio.run(app, debug=True)
