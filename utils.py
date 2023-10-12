import psutil

def get_top_processes(metric='cpu', top_n=5):
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)

    if metric == 'cpu':
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    else:
        processes.sort(key=lambda x: x['memory_percent'], reverse=True)

    return processes[:top_n]
