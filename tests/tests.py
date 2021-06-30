import unittest

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


class TestCountryRoute(unittest.TestCase):
    def test_fetch_private_ip_info(self):
        ip: str = "192.168.0.1"
        response = client.get(f"/country/{ip}")
        assert response.status_code == 400
        assert response.json() == {
            "detail": "The IP address '192.168.0.1' is a reserved IP address (private, multicast, etc.)."}

    def test_fetch_invalid_ip(self):
        ip: str = "555.168.0.1"
        response = client.get(f"/country/{ip}")
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid IP-address provided"}

    def test_fetch_unknown_ip(self):
        ip: str = "144.1.58.8"
        response = client.get(f"/country/{ip}")
        assert response.status_code == 404
        assert response.json() == {"detail": "The supplied IP address is not in the geolite database."}

    def test_fetch_valid_ip(self):
        ip: str = "144.48.22.1"
        response = client.get(f"/country/{ip}")
        assert response.status_code == 200
        assert response.json().get("country") is not None


if __name__ == '__main__':
    unittest.main()
