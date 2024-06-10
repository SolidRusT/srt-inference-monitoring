import multiprocessing
import os
import yaml
from prometheus_client import start_http_server

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def start_metrics_collector():
    os.system('python -m metrics.collector')

def start_flask_app():
    os.system('gunicorn -c gunicorn_config.py app.main:app')

def start_prometheus_server(port):
    start_http_server(port)

def main():
    config = load_config()
    metrics_port = config.get('metrics_port', 8000)  # Default to 8000 if not set

    p1 = multiprocessing.Process(target=start_metrics_collector)
    p2 = multiprocessing.Process(target=start_flask_app)
    p3 = multiprocessing.Process(target=start_prometheus_server, args=(metrics_port,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

if __name__ == '__main__':
    main()
