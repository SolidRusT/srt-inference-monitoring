import requests
import yaml
import logging
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from apscheduler.schedulers.background import BackgroundScheduler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Prometheus metrics
registry = CollectorRegistry()
cpu_usage = Gauge('cpu_usage', 'CPU Usage', registry=registry)
memory_usage = Gauge('memory_usage', 'Memory Usage', registry=registry)
gpu_usage = Gauge('gpu_usage', 'GPU Usage', registry=registry)

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def collect_metrics():
    config = load_config()
    for server in config['servers']:
        try:
            response = requests.get(server['address'] + '/metrics')
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()

            # Set metrics based on the response data
            cpu_usage.set(data['cpu_usage'])
            memory_usage.set(data['memory_usage'])
            gpu_usage.set(data['gpu_usage'])

            # Push metrics to Prometheus gateway
            push_to_gateway('localhost:9091', job=server['name'], registry=registry)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error collecting metrics from {server['name']}: {e}")

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_metrics, 'interval', seconds=30)  # Adjust the interval as needed
    scheduler.start()
    
    try:
        while True:
            pass  # Keep the main thread alive
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
