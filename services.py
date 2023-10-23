from redis import Redis
from utils import get_public_ip
from mail_service import send_email_notification

redis_store = Redis(host='localhost', port=6379, db=0)

def check_ip_change():
    current_ip = get_public_ip()
    previous_ip = redis_store.get("previous_ip").decode('utf-8')
        
    if current_ip and current_ip != previous_ip:
        send_email_notification("IP_Change", f"Public IP changed from {previous_ip} to {current_ip}")
        redis_store.set("previous_ip", current_ip)
    else:
        send_email_notification("IP_Change", f"Public IP hasn't changed")
        

if __name__ == "__main__":
    check_ip_change()
