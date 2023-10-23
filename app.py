from flask import Flask
from extensions import db, migrate, socketio, redis_store
from routes import register_blueprints
from background_tasks import start_background_tasks
from flask_cors import CORS
from models import get_last_5_spikes
from dotenv import load_dotenv
import os


def create_app():
    app = Flask(__name__)
    configure_app(app)
    register_extensions(app)
    register_blueprints(app)
    CORS(app)    
    return app

def configure_app(app):
    load_dotenv()    
    username = os.environ.get('MARIADB_USER')    
    password = os.environ.get('MARIADB_PASSWORD')
    hostname = os.environ.get('MARIADB_HOST')
    port =  os.environ.get('MARIADB_PORT')
    
    app.config['threaded'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/LCARS'    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['REDIS_URL'] = "redis://localhost:6379/0"    
    app.debug = True

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)    
    socketio.init_app(app, engineio_logger=True, cors_allowed_origins="*", supports_credentials=True)
    redis_store.init_app(app)

@socketio.on('connect', namespace='/events')
def handle_connect():
    print("Connected")
    last_5_spikes = get_last_5_spikes()    
    socketio.emit('initial_spikes', last_5_spikes, namespace='/events')

@socketio.on_error_default
def default_error_handler(e):
    print("An error occurred:", e)
    
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  
        start_background_tasks(app)
    socketio.run(app, host='0.0.0.0', port=8080) #5000 #8080



