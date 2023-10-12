from extensions import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
class SystemStat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    cpu_percentage = db.Column(db.Float, nullable=False)
    memory_percentage = db.Column(db.Float, nullable=False)
    storage_percentage = db.Column(db.Float, nullable=False)
    