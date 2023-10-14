import threading
from models import Event, SystemStat
from utils import get_top_processes
from extensions import db, socketio  # Import db and socketio from extensions
import time
import psutil
from mail_service import send_email_notification

def background_monitoring(app):
    with app.app_context():    
        while True:
            cpu_percentage = psutil.cpu_percent(interval=1) 
            memory_info = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            temp = psutil.sensors_temperatures()["cpu_thermal"][0].current
            time_stamp =     time.strftime("%Y-%m-%d %H:%M:%S")
            
            if cpu_percentage > 80:
                top_cpu_processes = get_top_processes(metric='cpu', top_n=3)
                event = f"High CPU usage detected: {cpu_percentage}%. Top processes: {', '.join([proc['name'] for proc in top_cpu_processes])}"
                new_event = Event(timestamp=time_stamp, description=event)
                db.session.add(new_event)
                db.session.commit()            
                socketio.emit('new_event', [time_stamp, event], namespace='/events')
                send_email_notification("CPU_overload", f"{time_stamp}-{event}")
            if memory_info > 60:
                top_memory_processes = get_top_processes(metric='memory', top_n=3)
                event = f"High memory usage detected: {memory_info.percent}%. Top processes: {', '.join([proc['name'] for proc in top_memory_processes])}"
                new_event = Event(timestamp=time_stamp, description=event)
                db.session.add(new_event)
                db.session.commit()  
                socketio.emit('new_event', [time_stamp, event], namespace='/events')
                send_email_notification("Memory_overload", f"{time_stamp}-{event}")
            if disk > 40:
                event = f"High disk usage detected: {disk}%."
                new_event = Event(timestamp=time_stamp, description=event)
                db.session.add(new_event)
                db.session.commit()
                socketio.emit('new_event', [time_stamp, event], namespace='/events')
                send_email_notification("Disk_overload", f"{time_stamp}-{event}")

            if temp > 45:  
                event = f"High CPU temperature detected: {temp}°C."
                new_event = Event(timestamp=time_stamp, description=event)
                db.session.add(new_event)
                db.session.commit()
                socketio.emit('new_event', [time_stamp, event], namespace='/events')
                send_email_notification("High_CPU_Temperature", f"{time_stamp}-{event}")


            # Maybe I should store temp too
            stat = SystemStat(
                timestamp=time_stamp,
                cpu_percentage= cpu_percentage,
                memory_percentage= memory_info,
                storage_percentage= disk
            )
            db.session.add(stat)
            db.session.commit()
            
            time.sleep(1)

def start_background_tasks(app):
    thread = threading.Thread(target=background_monitoring, args=(app,))
    thread.start()

