from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_redis import FlaskRedis
from flask_migrate import Migrate

db = SQLAlchemy()
socketio = SocketIO()
redis_store = FlaskRedis()
migrate = Migrate()
