# Performance Monitor

## Overview

This tool monitors the performance of a set of machines in a local network. It collects metrics using Prometheus and displays them on a Flask-based dashboard.

## Features

- Real-time performance monitoring
- Metrics collection using Prometheus
- Dashboard visualization with Flask and Chart.js

## Prerequisites

1. **Python 3.11**
2. **Prometheus Gateway** running on `localhost:9091`
3. **Prometheus Node Exporter** installed and running on each node (refer to `NODES.md` for setup instructions)
4. **Redis** server running on your local machine or accessible from it

## Configuration

1. **Copy the example configuration file**:

   ```bash
   cp config-example.yaml config.yaml
   ```

2. **Edit `config.yaml`** with your server details:

   ```yaml
   servers:
     - name: ServerOne
       address: http://ServerOne:9100
     - name: ServerTwo
       address: http://ServerTwo:9100

   dashboard:
     host: 0.0.0.0
     port: 5000
     debug: true

   metrics_port: 8000

   redis:
     host: localhost
     port: 6379
     db: 0
   ```

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/SolidRusT/srt-inference-monitoring.git
   cd srt-inference-monitoring
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Prometheus gateway**:
   Ensure that the Prometheus gateway is running on `localhost:9091`.

2. **Start the metrics collector and Flask application using Gunicorn**:

   ```bash
   python start.py
   ```

3. **Access the dashboard**:
   Open a web browser and navigate to `http://localhost:5000`.

## Running Tests

1. **Run unit tests**:

   ```bash
   python -m unittest discover tests
   ```

## Logging

Logs will provide information about the metrics collection process and any errors encountered. Check the logs for messages confirming that metrics are being collected and pushed to the Prometheus gateway.

## Troubleshooting

- **Metrics not displaying**: Ensure that the Prometheus gateway is running and accessible. Check the logs for any errors in metrics collection.
- **Scheduler not running**: Confirm that the scheduler is starting and running the `collect_metrics` function.

## License

MIT License. See `LICENSE` for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Author

Suparious, SolidRusT Networks
