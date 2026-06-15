import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from src.app import app


class TestAppEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")


class TestSustainabilityFixed(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("src.apis.sustainability.MetricsRepository.get_global_metrics")
    @patch("src.apis.sustainability.MetricsRepository.get_recent_metrics")
    @patch("src.apis.sustainability.MetricsRepository.get_endpoints_ranking")
    def test_environmental_impact_with_400_status(self, mock_ranking, mock_recent, mock_global):
        mock_global.return_value = {"total_requests": 50, "total_co2": 0.01, "avg_co2": 0.0002}
        mock_recent.return_value = [{
            "timestamp": "2023-10-27 10:00:00",
            "method": "GET",
            "path": "/api/test",
            "status_code": 404,
            "response_time_ms": 10.0,
            "bytes_transferred": 200,
            "co2_estimated": 0.0001,
        }]
        mock_ranking.return_value = []
        response = self.client.get("/environmental-impact")
        self.assertEqual(response.status_code, 200)

    @patch("src.apis.sustainability.MetricsRepository.get_global_metrics")
    @patch("src.apis.sustainability.MetricsRepository.get_recent_metrics")
    @patch("src.apis.sustainability.MetricsRepository.get_endpoints_ranking")
    def test_environmental_impact_empty_metrics(self, mock_ranking, mock_recent, mock_global):
        mock_global.return_value = {}
        mock_recent.return_value = []
        mock_ranking.return_value = []
        response = self.client.get("/environmental-impact")
        self.assertEqual(response.status_code, 200)

    @patch("os.path.exists", return_value=True)
    @patch("src.apis.sustainability.aiofiles")
    def test_greenframe_report_found(self, mock_aiofiles, mock_exists):
        import json
        mock_file = AsyncMock()
        mock_file.read = AsyncMock(return_value=json.dumps({"score": 90}))
        mock_aiofiles.open.return_value.__aenter__ = AsyncMock(return_value=mock_file)
        mock_aiofiles.open.return_value.__aexit__ = AsyncMock(return_value=False)
        response = self.client.get("/api/sustainability")
        self.assertEqual(response.status_code, 200)

    @patch("os.path.exists")
    def test_greenframe_report_not_found(self, mock_exists):
        mock_exists.return_value = False
        response = self.client.get("/api/sustainability")
        self.assertEqual(response.status_code, 404)

    @patch("os.path.exists")
    def test_greenframe_report_both_paths_missing(self, mock_exists):
        mock_exists.return_value = False
        response = self.client.get("/api/sustainability")
        self.assertEqual(response.status_code, 404)
        self.assertIn("GreenFrame", response.json()["message"])


if __name__ == '__main__':
    unittest.main()
