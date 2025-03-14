import pytest
import requests
from http import HTTPStatus
from app.models.User import *


class TestSmoke:
    def test_status_healthcheck(self, app_url: str) -> None:
        response = requests.get(f"{app_url}/status", timeout=5)
        assert response.status_code == HTTPStatus.OK
        assert response.json()["users"] is True

    @pytest.mark.parametrize("endpoint, expected_status", [
        ("/api/users", HTTPStatus.OK)
    ])
    def test_api_endpoints(
            self,
            app_url: str,
            endpoint: str,
            expected_status: HTTPStatus
    ) -> None:
        response = requests.get(f"{app_url}{endpoint}", timeout=5)
        assert response.status_code == expected_status

        if endpoint == "/api/users":
            Users.model_validate(response.json())
