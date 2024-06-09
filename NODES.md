# Node Setup for Performance Monitoring

This document outlines the steps required to prepare each node (server) for performance monitoring using Prometheus Node Exporter. Follow these instructions to ensure that each node is configured correctly and can report metrics to the monitoring server.

## Prerequisites

- Each node should be running Ubuntu 24.04 LTS.
- The monitoring server should have Prometheus and the Performance Monitor application set up.

## Steps to Set Up Prometheus Node Exporter on Each Node

### 1. Update the Package List

Ensure that your package list is up-to-date.

```bash
sudo apt update
```

### 2. Install Prometheus Node Exporter

Install Prometheus Node Exporter using the package manager.

```bash
sudo apt install prometheus-node-exporter
```

### 3. Configure Prometheus Node Exporter

The default configuration is generally sufficient for basic metrics collection. However, you can customize it if needed by editing the configuration file:

```bash
sudo nano /etc/default/prometheus-node-exporter
```

### 4. Start and Enable the Node Exporter Service

Start the Prometheus Node Exporter service and enable it to start on boot.

```bash
# Start the Prometheus Node Exporter service
sudo systemctl start prometheus-node-exporter

# Enable the service to start on boot
sudo systemctl enable prometheus-node-exporter

# Verify that the service is running
sudo systemctl status prometheus-node-exporter
```

### 5. Verify Node Exporter Installation

Check that Prometheus Node Exporter is running and listening on the default port (`9100`).

```bash
curl http://localhost:9100/metrics
```

You should see a list of metrics being collected by Prometheus Node Exporter.

## Example Systemd Service Configuration

If you need to customize the Node Exporter service, you can create or edit the systemd service file.

```bash
sudo nano /etc/systemd/system/prometheus-node-exporter.service
```

### Example Service Configuration

```ini
[Unit]
Description=Prometheus Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
ExecStart=/usr/bin/prometheus-node-exporter \
  --collector.cpu \
  --collector.diskstats \
  --collector.filesystem \
  --collector.loadavg \
  --collector.meminfo \
  --collector.netdev \
  --collector.stat \
  --collector.systemd \
  --collector.time \
  --collector.uname \
  --collector.vmstat \
  --collector.xfs \
  --collector.zfs

[Install]
WantedBy=default.target
```

After editing the service file, reload the systemd daemon and restart the Node Exporter service.

```bash
sudo systemctl daemon-reload
sudo systemctl restart prometheus-node-exporter
```

## Adding Nodes to `config.yaml`

Once Prometheus Node Exporter is set up and running on each node, update the `config.yaml` file on the monitoring server to include these nodes.

### Example `config.yaml`

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

## Final Steps

1. **Ensure that Prometheus Node Exporter is running on each node**.
2. **Update the `config.yaml` file on the monitoring server with the correct addresses for the Node Exporters**.
3. **Follow the steps outlined in the `README.md` and `TESTING.md` files to start the metrics collector, Flask application, and access the dashboard**.

By following these steps, you can ensure that each node is properly set up to report metrics to the monitoring server, allowing you to monitor the performance of your nodes effectively.
