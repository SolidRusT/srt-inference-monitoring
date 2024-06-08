# Performance Monitor

## Overview

This tool monitors the performance of a set of machines in a local network. It collects metrics using Prometheus and displays them on a Flask-based dashboard.

## Features

- Real-time performance monitoring
- Metrics collection using Prometheus
- Dashboard visualization with Flask

## Configuration

All configurable parameters are stored in `config.yaml`.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
gunicorn -c gunicorn_config.py app.main:app
```

## License

MIT License. See `LICENSE` for more details.
