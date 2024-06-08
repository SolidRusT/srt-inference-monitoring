import requests
import yaml
from .prometheus_client import cpu_usage

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def collect_metrics():
    config = load_config()
    for server in config['servers']:
        response = requests.get(server['address'] + '/metrics')
        if response.status_code == 200:
            data = response.json()
            cpu_usage.set(data['cpu_usage'])
            # Push metrics to Prometheus gateway
            push_to_gateway('localhost:9091', job=server['name'], registry=cpu_usage._registry)
