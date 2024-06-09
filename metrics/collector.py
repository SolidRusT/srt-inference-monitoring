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

def parse_prometheus_metrics(metrics_text):
    data = {}
    for line in metrics_text.splitlines():
        if line.startswith('#') or not line:
            continue
        parts = line.split()
        if len(parts) == 2:
            key, value = parts
            try:
                data[key] = float(value)
            except ValueError:
                logger.warning(f"Could not convert value to float: {value}")
                continue
    return data

def collect_metrics(redis_client):
    logger.info("Collecting metrics")
    config = load_config()
    for server in config['servers']:
        if server['name'] not in metrics:
            initialize_metrics(server['name'])
        try:
            response = requests.get(server['address'] + '/metrics')
            response.raise_for_status()
            data = parse_prometheus_metrics(response.text)
            logger.info(f"Collected metrics from {server['name']}: {data}")
            metrics[server['name']]['cpu_usage'].set(data.get('node_cpu_seconds_total', 0))
            metrics[server['name']]['memory_usage'].set(data.get('node_memory_MemTotal_bytes', 0))
            metrics[server['name']]['gpu_usage'].set(data.get('nvidia_gpu_usage', 0))
            # Cache metrics in Redis
            redis_client.set(f'{server["name"]}_cpu_usage', data.get('node_cpu_seconds_total', 0))
            redis_client.set(f'{server["name"]}_memory_usage', data.get('node_memory_MemTotal_bytes', 0))
            redis_client.set(f'{server["name"]}_gpu_usage', data.get('nvidia_gpu_usage', 0))
            # Log Redis cache
            logger.info(f"Cached metrics for {server['name']} in Redis")
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
