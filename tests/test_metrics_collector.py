import unittest
from prometheus.metrics_collector import load_config, collect_metrics

class TestMetricsCollector(unittest.TestCase):

    def test_load_config(self):
        config = load_config()
        self.assertIn('servers', config)

    def test_collect_metrics(self):
        # Mock the requests and Prometheus client here
        self.assertTrue(True)  # Placeholder for actual test logic

if __name__ == '__main__':
    unittest.main()
