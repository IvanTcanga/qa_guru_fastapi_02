import pytest
import requests
from http import HTTPStatus


class TestSmoke:
    def test_service_availability(self, app_url):
        response = requests.get(f"{app_url}/status")
        assert response.status_code == HTTPStatus.OK
        assert response.json()["users"] is True

    def test_service_endpoints(self, app_url):
        endpoints = ["/status", "/api/users"]
        for endpoint in endpoints:
            response = requests.get(f"{app_url}{endpoint}")
            assert response.status_code == HTTPStatus.OK
