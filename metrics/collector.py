import os
import requests
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from redis import Redis
from metrics.prometheus_metrics import registry, metrics
from metrics.config import load_config
from metrics.metrics_initializer import initialize_metrics
from metrics.metric_parsers import parse_prometheus_metrics
from metrics.metric_aggregators import aggregate_cpu_usage, aggregate_disk_usage, aggregate_network_io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            metrics[f'{server["name"]}_cpu_usage'].set(cpu_usage)
            metrics[f'{server["name"]}_memory_usage'].set(data.get('node_memory_MemTotal_bytes', 0))
            metrics[f'{server["name"]}_gpu_usage'].set(data.get('nvidia_gpu_utilization', 0))  # Ensure correct key
            metrics[f'{server["name"]}_disk_usage'].set(disk_usage)
            metrics[f'{server["name"]}_network_io'].set(network_io)
            # Cache metrics in Redis
            redis_client.set(f'{server["name"]}_cpu_usage', cpu_usage)
            redis_client.set(f'{server["name"]}_memory_usage', data.get('node_memory_MemTotal_bytes', 0))
            redis_client.set(f'{server["name"]}_gpu_usage', data.get('nvidia_gpu_utilization', 0))
            redis_client.set(f'{server["name"]}_disk_usage', disk_usage)
            redis_client.set(f'{server["name"]}_network_io', network_io)
            # Log Redis cache
            logger.info(f"Cached metrics for {server['name']} in Redis")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error collecting metrics from {server['name']}: {e}")

if __name__ == "__main__":
    config = load_config()
    redis_host = os.getenv('VALKEY_HOST', config.get('redis', {}).get('host', 'localhost'))
    redis_client = Redis(
        host=redis_host,
        port=config.get('redis', {}).get('port', 6379),
        db=config.get('redis', {}).get('db', 0)
    )
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
