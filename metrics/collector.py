import requests
import yaml
import logging
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from apscheduler.schedulers.background import BackgroundScheduler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Prometheus metrics
registries = {}
metrics = {}

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def initialize_metrics(server_name):
    logger.info(f"Initializing metrics for server: {server_name}")
    registry = CollectorRegistry()
    metrics[server_name] = {
        'cpu_usage': Gauge(f'{server_name}_cpu_usage', 'CPU Usage', registry=registry),
        'memory_usage': Gauge(f'{server_name}_memory_usage', 'Memory Usage', registry=registry),
        'gpu_usage': Gauge(f'{server_name}_gpu_usage', 'GPU Usage', registry=registry),
    }
    registries[server_name] = registry

def collect_metrics():
    logger.info("Collecting metrics")
    config = load_config()
    for server in config['servers']:
        if server['name'] not in metrics:
            initialize_metrics(server['name'])
        try:
            response = requests.get(server['address'] + '/metrics')
            response.raise_for_status()
            data = response.json()
            logger.info(f"Collected metrics from {server['name']}: {data}")
            metrics[server['name']]['cpu_usage'].set(data['cpu_usage'])
            metrics[server['name']]['memory_usage'].set(data['memory_usage'])
            metrics[server['name']]['gpu_usage'].set(data['gpu_usage'])
            push_to_gateway('localhost:9091', job=server['name'], registry=registries[server['name']])
        except requests.exceptions.RequestException as e:
            logger.error(f"Error collecting metrics from {server['name']}: {e}")

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_metrics, 'interval', seconds=30)
    scheduler.start()
    logger.info("Scheduler started")
    try:
        while True:
            pass  # Keep the main thread alive
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped")
 