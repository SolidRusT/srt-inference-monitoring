# Prometheus Setup

This document outlines the steps required to set up Prometheus for collecting and visualizing metrics from your nodes and the metrics collector.

## Prerequisites

1. **Prometheus**
2. **Prometheus Node Exporter** installed and running on each node (refer to `NODES.md` for setup instructions)

## Prometheus Setup

### 1. Install Prometheus

Follow the installation instructions for your operating system from the [Prometheus download page](https://prometheus.io/download/).

### 2. Create Prometheus Configuration File

Create a configuration file named `prometheus.yml` in the Prometheus installation directory.

#### Example `prometheus.yml`

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['erebus:9100', 'thanatos:9100', 'zelus:9100', 'orpheus:9100', 'hades:9100']

  - job_name: 'metrics_collector'
    static_configs:
      - targets: ['localhost:8000']  # Assuming your metrics collector exposes metrics on localhost:8000
```
