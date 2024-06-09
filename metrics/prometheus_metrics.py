from prometheus_client import CollectorRegistry, Gauge

# Singleton instance of the Prometheus CollectorRegistry
registry = CollectorRegistry()

# Dictionary to hold the metrics for each server
metrics = {}

def initialize_metric(server_name, metric_name, description):
    """Initialize a metric for a given server.
    
    Args:
        server_name (str): The name of the server.
        metric_name (str): The name of the metric.
        description (str): The description of the metric.
    
    Returns:
        Gauge: The initialized Prometheus Gauge metric.
    """
    full_metric_name = f'{server_name}_{metric_name}'
    if full_metric_name not in metrics:
        metrics[full_metric_name] = Gauge(full_metric_name, description, registry=registry)
    return metrics[full_metric_name]
