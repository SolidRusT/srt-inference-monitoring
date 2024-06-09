import requests
import yaml
import logging
from prometheus_client import start_http_server
from apscheduler.schedulers.background import BackgroundScheduler
from redis import Redis
from metrics.prometheus_metrics import registry, initialize_metric, metrics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def initialize_metrics(server_name):
    logger.info(f"Initializing metrics for server: {server_name}")
    initialize_metric(server_name, 'cpu_usage', 'CPU Usage')
    initialize_metric(server_name, 'memory_usage', 'Memory Usage')
    initialize_metric(server_name, 'gpu_usage', 'GPU Usage')
    initialize_metric(server_name, 'disk_usage', 'Disk Usage')
    initialize_metric(server_name, 'network_io', 'Network I/O')

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

def aggregate_cpu_usage(data):
    cpu_keys = [key for key in data.keys() if 'node_cpu_seconds_total' in key]
    cpu_usage = sum(data[key] for key in cpu_keys)
    return cpu_usage

def aggregate_disk_usage(data):
    disk_keys = [key for key in data.keys() if 'node_filesystem_avail_bytes' in key]
    disk_usage = sum(data[key] for key in disk_keys)
    return disk_usage

def aggregate_network_io(data):
    network_receive_keys = [key for key in data.keys() if 'node_network_receive_bytes_total' in key]
    network_transmit_keys = [key for key in data.keys() if 'node_network_transmit_bytes_total' in key]
    network_io = sum(data[key] for key in network_receive_keys + network_transmit_keys)
    return network_io

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
            cpu_usage = aggregate_cpu_usage(data)
            disk_usage = aggregate_disk_usage(data)
            network_io = aggregate_network_io(data)
            gpu_usage = data.get('dcgm_gpu_utilization', 0)  # Fetch GPU utilization from Prometheus
            metrics[f'{server["name"]}_cpu_usage'].set(cpu_usage)
            metrics[f'{server["name"]}_memory_usage'].set(data.get('node_memory_MemTotal_bytes', 0))
            metrics[f'{server["name"]}_gpu_usage'].set(gpu_usage)
            metrics[f'{server["name"]}_disk_usage'].set(disk_usage)
            metrics[f'{server["name"]}_network_io'].set(network_io)
            # Cache metrics in Redis
            redis_client.set(f'{server["name"]}_cpu_usage', cpu_usage)
            redis_client.set(f'{server["name"]}_memory_usage', data.get('node_memory_MemTotal_bytes', 0))
            redis_client.set(f'{server["name"]}_gpu_usage', gpu_usage)
            redis_client.set(f'{server["name"]}_disk_usage', disk_usage)
            redis_client.set(f'{server["name"]}_network_io', network_io)
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
