import logging
from metrics.prometheus_metrics import initialize_metric

# Configure logging
logger = logging.getLogger(__name__)

def initialize_metrics(server_name):
    logger.info(f"Initializing metrics for server: {server_name}")
    initialize_metric(server_name, 'cpu_usage', 'CPU Usage')
    initialize_metric(server_name, 'memory_usage', 'Memory Usage')
    initialize_metric(server_name, 'gpu_usage', 'GPU Usage')
    initialize_metric(server_name, 'disk_usage', 'Disk Usage')
    initialize_metric(server_name, 'network_io', 'Network I/O')
