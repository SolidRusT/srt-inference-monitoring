# NODES Setup

This document outlines the steps required to prepare each node for monitoring by the Performance Monitor application.

## Install Prometheus Node Exporter

1. **Download and install Node Exporter**:

    ```bash
    sudo apt-get update
    sudo apt-get install -y prometheus-node-exporter
    ```

2. **Create a systemd service file for Node Exporter**:

    ```bash
    sudo nano /etc/systemd/system/node_exporter.service
    ```

    Add the following content:

    ```ini
    [Unit]
    Description=Node Exporter
    Wants=network-online.target
    After=network-online.target

    [Service]
    User=nodeusr
    ExecStart=/usr/bin/prometheus-node-exporter
    Restart=always

    [Install]
    WantedBy=default.target
    ```

3. **Reload systemd, start and enable Node Exporter**:

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start node_exporter
    sudo systemctl enable node_exporter
    ```

## Install Prometheus NVIDIA Exporter

To monitor GPU usage, install the NVIDIA DCGM exporter on each machine with an NVIDIA GPU.

1. **Install NVIDIA DCGM**:

    ```bash
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.2.89-1_amd64.deb
    sudo dpkg -i cuda-repo-ubuntu1804_10.2.89-1_amd64.deb
    sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
    sudo apt-get update
    sudo apt-get install -y datacenter-gpu-manager
    ```

2. **Install the NVIDIA DCGM exporter**:

    ```bash
    wget https://github.com/NVIDIA/dcgm-exporter/releases/download/v2.0.13-2.3.0/nvidia-dcgm-exporter_2.0.13-2.3.0_amd64.deb
    sudo dpkg -i nvidia-dcgm-exporter_2.0.13-2.3.0_amd64.deb
    ```

3. **Create a systemd service file for NVIDIA DCGM exporter**:

    ```bash
    sudo nano /etc/systemd/system/dcgm-exporter.service
    ```

    Add the following content:

    ```ini
    [Unit]
    Description=NVIDIA DCGM Exporter
    Wants=network-online.target
    After=network-online.target

    [Service]
    User=nvidiauser
    ExecStart=/usr/bin/dcgm-exporter
    Restart=always

    [Install]
    WantedBy=default.target
    ```

4. **Reload systemd, start and enable NVIDIA DCGM exporter**:

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start dcgm-exporter
    sudo systemctl enable dcgm-exporter
    ```

## Verifying Prometheus Configuration

Ensure the Prometheus Node Exporter and NVIDIA DCGM exporter are running and exposing metrics at `http://<server_address>:9100/metrics`.

### Verify GPU Metrics

1. **Check GPU metrics**:

    ```bash
    curl http://localhost:9100/metrics | grep 'dcgm_gpu_utilization'
    ```

By following these steps, you can ensure that the nodes are correctly set up to expose the required metrics for monitoring.
