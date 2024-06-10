from prometheus_client import start_http_server
from metrics.prometheus_metrics import registry
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    port = 8000
    start_http_server(port, registry=registry)
    logger.info(f"Prometheus server started on port {port}")
    try:
        while True:
            pass  # Keep the main thread alive
    except (KeyboardInterrupt, SystemExit):
        logger.info("Prometheus server stopped")

if __name__ == "__main__":
    main()
