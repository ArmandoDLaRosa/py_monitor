import psutil
import requests

def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        return response.json()['origin']
    except Exception as e:
        print(f"Error retrieving public IP: {e}")
        return None
    
def get_top_processes(metric='cpu', top_n=5):
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)

    if metric == 'cpu':
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    else:
        processes.sort(key=lambda x: x['memory_percent'], reverse=True)

    return processes[:top_n]
