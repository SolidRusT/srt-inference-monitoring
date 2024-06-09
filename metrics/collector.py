import requests
import yaml
import logging
from prometheus_client import CollectorRegistry, Gauge, start_http_server
from apscheduler.schedulers.background import BackgroundScheduler
from redis import Redis
from metrics.prometheus_metrics import registry, metrics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def initialize_metrics(server_name):
    logger.info(f"Initializing metrics for server: {server_name}")
    metrics[server_name] = {
        'cpu_usage': Gauge(f'{server_name}_cpu_usage', 'CPU Usage', registry=registry),
        'memory_usage': Gauge(f'{server_name}_memory_usage', 'Memory Usage', registry=registry),
        'gpu_usage': Gauge(f'{server_name}_gpu_usage', 'GPU Usage', registry=registry),
    }

def collect_metrics(redis_client):
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
            # Cache metrics in Redis
            redis_client.set(f'{server["name"]}_cpu_usage', data['cpu_usage'])
            redis_client.set(f'{server["name"]}_memory_usage', data['memory_usage'])
            redis_client.set(f'{server["name"]}_gpu_usage', data['gpu_usage'])
        except requests.exceptions.RequestException as e:
            logger.error(f"Error collecting metrics from {server['name']}: {e}")

if __name__ == "__main__":
    config = load_config()
    metrics_port = config.get('metrics_port', 8000)
    redis_config = config.get('redis', {})
    redis_client = Redis(
        host=redis_config.get('host', 'localhost'),
        port=redis_config.get('port', 6379),
        db=redis_config.get('db', 0)
    )
    start_http_server(metrics_port, registry=registry)  # Expose metrics on specified port
    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_metrics, 'interval', seconds=30, args=[redis_client])
    scheduler.start()
    logger.info("Scheduler started")
    try:
        while True:
            pass  # Keep the main thread alive
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped")
