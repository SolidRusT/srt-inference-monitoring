from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()

# Example gauge, you can define more metrics as needed
cpu_usage = Gauge('cpu_usage', 'CPU Usage', registry=registry)
