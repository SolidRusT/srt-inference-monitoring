from flask import Blueprint, render_template, jsonify
import logging
import prometheus_client
from prometheus.metrics_collector import metrics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    return render_template('dashboard.html')

@main.route('/api/metrics')
def get_metrics():
    data = {server: {metric: gauge.collect()[0].samples[0].value for metric, gauge in server_metrics.items()} 
            for server, server_metrics in metrics.items()}
    logger.info(f"Returning metrics data: {data}")
    return jsonify(data)
