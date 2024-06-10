import unittest
from flask import Flask
from app.routes import main
from metrics.prometheus_metrics import initialize_metric, metrics

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__, template_folder="../app/templates")
        self.app.register_blueprint(main)
        self.client = self.app.test_client()
    
    def test_dashboard_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Performance Dashboard', response.data)
    
    def test_metrics_route(self):
        response = self.client.get('/metrics')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('Erebus', data)  # Example check
        self.assertIn('cpu_usage', data['Erebus'])

if __name__ == '__main__':
    unittest.main()
