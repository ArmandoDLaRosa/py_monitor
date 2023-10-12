from flask import Flask
from extensions import db, socketio
from routes import register_blueprints
from background_tasks import start_background_tasks
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    configure_app(app)
    register_extensions(app)
    register_blueprints(app)
    CORS(app)    
    return app

def configure_app(app):
    app.config['threaded'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rasp4_armando.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.debug = True

def register_extensions(app):
    db.init_app(app)
    socketio.init_app(app, engineio_logger=True, cors_allowed_origins="*", supports_credentials=True)

@socketio.on('connect', namespace='/events')
def handle_connect():
    print('Client connected')

@socketio.on_error_default
def default_error_handler(e):
    print("An error occurred:", e)
    
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        start_background_tasks(app)
    socketio.run(app, host='0.0.0.0', port=5000)



