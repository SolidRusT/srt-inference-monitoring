import multiprocessing
import os

def start_metrics_collector():
    os.system('python -m metrics.collector')

def start_flask_app():
    os.system('gunicorn -c gunicorn_config.py app.main:app')

def start_prometheus_server():
    os.system('python start_prometheus_server.py')

def main():
    p1 = multiprocessing.Process(target=start_metrics_collector)
    p2 = multiprocessing.Process(target=start_flask_app)
    p3 = multiprocessing.Process(target=start_prometheus_server)

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

if __name__ == '__main__':
    main()
