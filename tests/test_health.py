import unittest
import json
from app import create_app


class HealthCheckTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app({"TESTING": True, "DATABASE": ":memory:"})
        self.client = self.app.test_client()

    def test_health_returns_200(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

    def test_health_returns_json_status_ok(self):
        response = self.client.get("/health")
        data = json.loads(response.data)
        self.assertEqual(data, {"status": "ok"})

    def test_health_content_type_is_json(self):
        response = self.client.get("/health")
        self.assertIn("application/json", response.content_type)


if __name__ == "__main__":
    unittest.main()
