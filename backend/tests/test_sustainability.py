import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.app import app

class TestSustainability(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("src.apis.sustainability.MetricsRepository.get_global_metrics")
    @patch("src.apis.sustainability.MetricsRepository.get_recent_metrics")
    @patch("src.apis.sustainability.MetricsRepository.get_endpoints_ranking")
    def test_get_environmental_impact(self, mock_ranking, mock_recent, mock_global):
        mock_global.return_value = {
            "total_requests": 100,
            "total_co2": 0.05,
            "avg_co2": 0.0005
        }
        mock_recent.return_value = [
            {
                "timestamp": "2023-10-27 10:00:00",
                "method": "GET",
                "path": "/api/test",
                "status_code": 200,
                "response_time_ms": 15.0,
                "bytes_transferred": 500,
                "co2_estimated": 0.0001
            },
            {
                "timestamp": "2023-10-27 10:01:00",
                "method": "POST",
                "path": "/api/error",
                "status_code": 500,
                "response_time_ms": 20.0,
                "bytes_transferred": 100,
                "co2_estimated": 0.0002
            }
        ]
        mock_ranking.return_value = [{"method": "GET", "path": "/api/heavy"}]

        response = self.client.get("/environmental-impact")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn("Dashboard de Impacto Ambiental", response.text)
        self.assertIn("GET /api/heavy", response.text)
        self.assertIn("100", response.text)

    @patch("os.path.exists")
    def test_get_greenframe_report_not_found(self, mock_exists):
        mock_exists.return_value = False
        response = self.client.get("/api/sustainability")
        self.assertEqual(response.status_code, 404)
        self.assertIn("GreenFrame", response.json()["message"])

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{"score": 90}')
    def test_get_greenframe_report_found(self, mock_open, mock_exists):
        mock_exists.return_value = True
        response = self.client.get("/api/sustainability")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"score": 90})

if __name__ == '__main__':
    unittest.main()
