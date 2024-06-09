from flask import Blueprint, render_template, jsonify
import logging
from redis import Redis
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

config = load_config()
redis_config = config.get('redis', {})
redis_client = Redis(
    host=redis_config.get('host', 'localhost'),
    port=redis_config.get('port', 6379),
    db=redis_config.get('db', 0)
)

@main.route('/')
def dashboard():
    return render_template('dashboard.html')

@main.route('/api/metrics')
def get_metrics():
    data = {}
    for server in config['servers']:
        server_name = server['name']
        data[server_name] = {
            'cpu_usage': float(redis_client.get(f'{server_name}_cpu_usage') or 0),
            'memory_usage': float(redis_client.get(f'{server_name}_memory_usage') or 0),
            'gpu_usage': float(redis_client.get(f'{server_name}_gpu_usage') or 0)
        }
    logger.info(f"Returning metrics data: {data}")
    return jsonify(data)
