from extensions import db
from datetime import datetime
import json

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False,  index=True)  
    description = db.Column(db.String(500), nullable=False)
    
class SystemStat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False,  index=True)  
    cpu_percentage = db.Column(db.Float, nullable=False)
    memory_percentage = db.Column(db.Float, nullable=False)
    storage_percentage = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

def get_last_5_spikes():
    last_5_spikes = Event.query.order_by(Event.timestamp.desc()).limit(5).all()
    return json.dumps([{'timestamp': spike.timestamp,
                        'event': spike.description}
                       for spike in last_5_spikes], cls=DateTimeEncoder)