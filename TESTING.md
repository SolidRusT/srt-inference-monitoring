# Testing Workflow

This document outlines the steps required to test the Performance Monitor application. Follow these instructions to ensure the application is configured correctly, runs smoothly, and functions as expected.

## Testing Procedure

### 1. Verify Configuration

Ensure the `config.yaml` file is correctly configured with your server details.

#### Example `config.yaml`

```yaml
servers:
  - name: Erebus
    address: http://erebus:9100
  - name: Thanatos
    address: http://thanatos:9100
  - name: Zelus
    address: http://zelus:9100
  - name: Orpheus
    address: http://orpheus:9100

dashboard:
  host: 0.0.0.0
  port: 5000
  debug: true
```

### 2. Start Prometheus Gateway

Ensure the Prometheus gateway is running and accessible at `localhost:9091`.

#### Gateway command

```bash
# Ensure Prometheus gateway is running on localhost:9091
# Command to start Prometheus gateway, if necessary:
prometheus --config.file=prometheus.yml
```

### 3. Set Up Remote Servers

To enable metric collection, set up the Prometheus Node Exporter on each remote server. Refer to `NODES.md` for detailed instructions.

#### Steps for setting up Node Exporter

1. **Update the package list**:

   ```bash
   sudo apt update
   ```

2. **Install Prometheus Node Exporter**:

   ```bash
   sudo apt install prometheus-node-exporter
   ```

3. **Start and enable Node Exporter**:

   ```bash
   sudo systemctl start prometheus-node-exporter
   sudo systemctl enable prometheus-node-exporter
   ```

4. **Verify Node Exporter**:

   - Check the status:

     ```bash
     sudo systemctl status prometheus-node-exporter
     ```

   - Verify metrics are exposed at `http://<server_address>:9100/metrics`.

### 4. Run Metrics Collector

Start the metrics collector script to begin collecting metrics from the configured servers.

#### Collector command

```bash
python prometheus/metrics_collector.py
```

### 5. Start Flask Application

Use Gunicorn to start the Flask application.

#### Web service command

```bash
gunicorn -c gunicorn_config.py app.main:app
```

### 6. Access Dashboard

Open a web browser and navigate to `http://localhost:5000` to access the performance dashboard.

### 7. Verify Metrics Display

Ensure that the performance metrics for all configured servers are displayed correctly on the dashboard.

### 8. Run Unit Tests

Execute the unit tests to validate the functionality of the application components.

#### Unit testing command

```bash
python -m unittest discover tests
```

## Detailed Testing Workflow

### Prerequisites

1. **Python 3.11**: Ensure Python 3.11 is installed.
2. **Prometheus Gateway**: Prometheus gateway should be running on `localhost:9091`.

### Environment Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-repo/performance-monitor.git
   cd performance-monitor
   ```

2. **Create and Activate a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start Prometheus Gateway**:

   - Ensure Prometheus gateway is running. Use the appropriate command to start it if necessary.

2. **Run Metrics Collector**:

   - Start the metrics collector script to gather metrics from the servers.
   - Command:

     ```bash
     python prometheus/metrics_collector.py
     ```

3. **Start Flask Application**:

   - Use Gunicorn to start the Flask application.
   - Command:

     ```bash
     gunicorn -c gunicorn_config.py app.main:app
     ```

4. **Access and Verify Dashboard**:
   - Open a web browser and go to `http://localhost:5000`.
   - Verify that the dashboard displays the performance metrics for all configured servers.

### Running Tests

1. **Unit Tests**:

   - Run the unit tests to ensure all components are functioning correctly.
   - Command:

     ```bash
     python -m unittest discover tests
     ```

### Logging and Troubleshooting

1. **Check Logs**:

   - Review logs for messages confirming metrics collection and any errors encountered.
   - Ensure logs indicate successful metrics collection and data push to Prometheus gateway.

2. **Common Issues**:
   - **Metrics not displaying**: Verify Prometheus gateway is running and accessible. Check logs for errors.
   - **Scheduler not running**: Confirm scheduler is starting and running the `collect_metrics` function.

### Summary

By following these detailed steps, you can ensure that the Performance Monitor application is properly configured, running, and tested to verify its functionality.
