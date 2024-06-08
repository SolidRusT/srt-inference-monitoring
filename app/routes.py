from flask import Blueprint, render_template, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    return render_template('dashboard.html')

@main.route('/api/metrics')
def get_metrics():
    # Example static data, replace with real metrics collection
    data = {
        'cpu_usage': 55.0,
        'memory_usage': 70.0,
        'gpu_usage': 40.0
    }
    return jsonify(data)
