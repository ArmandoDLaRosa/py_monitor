from flask import Blueprint, render_template, jsonify
import psutil
import os
from models import SystemStat
import datetime
from sqlalchemy import func 

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/metrics')
def metrics():
    cpu_percentage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()

    try:
        temp = psutil.sensors_temperatures()["cpu_thermal"][0].current
    except:
        temp = "N/A"

    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    load_avg = os.getloadavg()

    return jsonify(
        cpu=cpu_percentage, 
        memory=memory_info.percent, 
        temperature=temp,
        disk_total=disk.total,
        disk_used=disk.used,
        disk_free=disk.free,
        disk_percent=disk.percent,
        bytes_sent=net.bytes_sent,
        bytes_received=net.bytes_recv,
        load_avg_1=load_avg[0],
        load_avg_5=load_avg[1],
        load_avg_15=load_avg[2]
    )
    
@main_bp.route('/historic-stats')
def historic_stats():
    today =  datetime.datetime.now()
    seven_days_ago = today - datetime.timedelta(days=7)

    hourly_stats_query = SystemStat.query.with_entities(
        func.date_format(SystemStat.timestamp, "%Y-%m-%d %H:00:00").label('hour'),
        func.max(SystemStat.cpu_percentage).label('max_cpu_percentage'),
        func.max(SystemStat.memory_percentage).label('max_memory_percentage'),
        func.max(SystemStat.storage_percentage).label('max_storage_percentage'),
        func.max(SystemStat.temperature).label('max_temperature')        
    ).filter(
        SystemStat.timestamp >= seven_days_ago,
        SystemStat.timestamp <= today
    ).group_by(
        func.date_format(SystemStat.timestamp, "%Y-%m-%d %H:00:00")
    ).order_by(
        func.date_format(SystemStat.timestamp, "%Y-%m-%d %H:00:00")
    ).all()

    hourly_stats = [{
        "timestamp": record.hour,
        "cpu_percentage": record.max_cpu_percentage,
        "memory_percentage": record.max_memory_percentage,
        "storage_percentage": record.max_storage_percentage,
        "temperature": record.max_temperature
    } for record in hourly_stats_query]

    return jsonify(hourly_stats)

def register_blueprints(app):
    app.register_blueprint(main_bp)
