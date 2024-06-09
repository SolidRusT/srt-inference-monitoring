from flask import Blueprint, jsonify, render_template
from redis import Redis
import yaml
import logging
import json

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

redis_config = config.get('redis', {})
redis_client = Redis(
    host=redis_config.get('host', 'localhost'),
    port=redis_config.get('port', 6379),
    db=redis_config.get('db', 0)
)

@main.route('/')
def dashboard():
    return render_template('dashboard.html')

@main.route('/metrics')
def get_metrics():
    data = {}
    for server in config['servers']:
        server_name = server['name']
        data[server_name] = {
            'cpu_usage': float(redis_client.get(f'{server_name}_cpu_usage') or 0),
            'memory_usage': float(redis_client.get(f'{server_name}_memory_usage') or 0),
            'gpu_usage': float(redis_client.get(f'{server_name}_gpu_usage') or 0),
            'disk_usage': float(redis_client.get(f'{server_name}_disk_usage') or 0),
            'network_io': float(redis_client.get(f'{server_name}_network_io') or 0),
        }
    logger.info(f"Returning metrics data: {data}")
    return jsonify(data)
