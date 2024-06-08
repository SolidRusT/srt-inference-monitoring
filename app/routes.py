from flask import Blueprint, render_template
import prometheus_client

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    # Render dashboard with real-time metrics
    return render_template('dashboard.html')
