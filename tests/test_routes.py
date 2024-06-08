import unittest
from app import create_app

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_dashboard_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_metrics(self):
        response = self.client.get('/api/metrics')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('cpu_usage', data)
        self.assertIn('memory_usage', data)
        self.assertIn('gpu_usage', data)

if __name__ == '__main__':
    unittest.main()
