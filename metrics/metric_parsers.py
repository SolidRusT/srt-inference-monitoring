import logging

# Configure logging
logger = logging.getLogger(__name__)

def parse_prometheus_metrics(metrics_text):
    data = {}
    for line in metrics_text.splitlines():
        if line.startswith('#') or not line:
            continue
        parts = line.split()
        if len(parts) == 2:
            key, value = parts
            try:
                data[key] = float(value)
            except ValueError:
                logger.warning(f"Could not convert value to float: {value}")
                continue
    return data
