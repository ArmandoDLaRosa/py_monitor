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
    # Calculate the datetime for 7 days ago from now
    seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    
    # Calculate the start and end of each hour for the last 7 days
    hours = [(seven_days_ago + datetime.timedelta(hours=i), seven_days_ago + datetime.timedelta(hours=i+1)) for i in range(24*7)]
    
    # Query the database to calculate the average metric for each hour
    hourly_stats = []
    for start_time, end_time in hours:
        avg_metric = SystemStat.query.with_entities(
            func.avg(SystemStat.cpu_percentage).label('avg_cpu_percentage'),
            func.avg(SystemStat.memory_percentage).label('avg_memory_percentage'),
            func.avg(SystemStat.storage_percentage).label('avg_storage_percentage')
        ).filter(
            SystemStat.timestamp >= start_time,
            SystemStat.timestamp < end_time
        ).first()
        
        if avg_metric:
            hourly_stats.append({
                "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "cpu_percentage": avg_metric.avg_cpu_percentage,
                "memory_percentage": avg_metric.avg_memory_percentage,
                "storage_percentage": avg_metric.avg_storage_percentage
            })

    return jsonify(hourly_stats)
    
def register_blueprints(app):
    app.register_blueprint(main_bp)
