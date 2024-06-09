import unittest
from app import create_app
from prometheus.metrics_collector import initialize_metrics, metrics

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        # Initialize metrics for testing
        initialize_metrics('test_server')
        metrics['test_server']['cpu_usage'].set(50.0)
        metrics['test_server']['memory_usage'].set(70.0)
        metrics['test_server']['gpu_usage'].set(40.0)

    def test_dashboard_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_metrics(self):
        response = self.client.get('/api/metrics')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('cpu_usage', data['test_server'])
        self.assertIn('memory_usage', data['test_server'])
        self.assertIn('gpu_usage', data['test_server'])

if __name__ == '__main__':
    unittest.main()
