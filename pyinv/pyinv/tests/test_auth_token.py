from datetime import datetime, timedelta

import jwt
import pytest
from django.contrib.auth.models import User

from pyinv.tests.client import Client


@pytest.mark.django_db
class TestAuthToken:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="user", password="password")

    @pytest.fixture
    def api_client(self) -> Client:
        return Client()

    def test_bad_request(self, api_client: Client) -> None:
        resp = api_client.post("/api/v1/auth/token/")
        assert resp.status_code == 400
        assert resp.json() == {'password': ['This field is required.'], 'username': ['This field is required.']}

    def test_bad_credentials(self, api_client: Client) -> None:
        resp = api_client.post("/api/v1/auth/token/", {"username": "user", "password": "bees"})
        assert resp.status_code == 401
        assert resp.json() == {'detail': 'No active account found with the given credentials'}

    def _check_token(self, token: str, *, token_type: str, expected_lt: timedelta) -> None:
        payload = jwt.decode(token, options={"verify_signature": False})
        assert payload["token_type"] == token_type
        iat = datetime.fromtimestamp(payload["iat"])
        exp = datetime.fromtimestamp(payload["exp"])
        lifetime = exp - iat
        assert lifetime == expected_lt

    @pytest.mark.usefixtures("user")
    def test_get_tokens(self, api_client: Client) -> None:
        resp = api_client.post("/api/v1/auth/token/", {"username": "user", "password": "password"})
        assert resp.status_code == 200
        data = resp.json()

        self._check_token(data["access"], token_type="access", expected_lt=timedelta(seconds=300))
        self._check_token(data["refresh"], token_type="refresh", expected_lt=timedelta(days=7))
