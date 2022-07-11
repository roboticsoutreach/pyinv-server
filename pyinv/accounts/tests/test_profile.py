import pytest
from django.contrib.auth.models import User

from pyinv.tests.client import Client


class TestProfileView:

    _subject = "/api/v1/accounts/profile/"

    public_user_attributes = {'username', 'first_name', 'last_name', 'email'}

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="user", password="password")

    @pytest.fixture
    def client(self) -> Client:
        return Client()

    @pytest.fixture
    def api_client(self, client: Client, user: User) -> Client:
        client.force_authenticate(user)
        return client

    def _add_user_details(self, user: User) -> None:
        user.first_name = "First Name"
        user.last_name = "Last Name"
        user.email = "first.last@example.com"
        user.save()

    def test_fetch_profile_no_auth(self, client: Client) -> None:
        resp = client.get(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'Authentication credentials were not provided.'}

    @pytest.mark.django_db
    def test_fetch_profile_minimal_info(self, user: User, api_client: Client) -> None:
        resp = api_client.get(self._subject)
        assert resp.status_code == 200
        data = resp.json()
        assert data.keys() == self.public_user_attributes
        assert data["username"] == "user"

        for attribute in ('first_name', 'last_name', 'email'):
            assert data[attribute] == ''

    @pytest.mark.django_db
    def test_fetch_profile(self, user: User, api_client: Client) -> None:
        self._add_user_details(user)
        resp = api_client.get(self._subject)
        assert resp.status_code == 200
        data = resp.json()

        assert data.keys() == self.public_user_attributes
        assert data["username"] == user.username
        assert data["first_name"] == user.first_name
        assert data["last_name"] == user.last_name
        assert data["email"] == user.email

    @pytest.mark.django_db
    def test_put_profile(self, user: User, api_client: Client) -> None:
        data = {
            "username": "foo",
            "first_name": "bar",
            "last_name": "bar2",
            "email": "email@example.com"
        }
        resp = api_client.put(self._subject, data=data)
        assert resp.status_code == 200
        assert resp.json() == data

        assert user.username == "foo"
        assert user.first_name == "bar"
        assert user.last_name == "bar2"
        assert user.email == "email@example.com"

    @pytest.mark.django_db
    def test_put_profile_missing_attrs(self, user: User, api_client: Client) -> None:
        data = {
            "last_name": "bar2",
            "email": "email@example.com"
        }
        resp = api_client.put(self._subject, data=data)
        assert resp.status_code == 400
        assert resp.json() == {'username': ['This field is required.']}

    @pytest.mark.django_db
    def test_put_profile_bad(self, user: User, api_client: Client) -> None:
        data = {
            "username": "user",
            "first_name": "",
            "last_name": "",
            "email": "not_an_email"
        }
        resp = api_client.put(self._subject, data=data)
        assert resp.status_code == 400
        assert resp.json() == {
            'first_name': ['Expected at least 1 character'],
            'last_name': ['Expected at least 1 character'],
            'email': ['Enter a valid email address.'],
        }

    @pytest.mark.django_db
    def test_patch_profile(self, user: User, api_client: Client) -> None:
        data = {
            "username": "foo",
            "first_name": "bar",
            "last_name": "bar2",
            "email": "email@example.com"
        }
        resp = api_client.patch(self._subject, data=data)
        assert resp.status_code == 200
        assert resp.json() == data

        assert user.username == "foo"
        assert user.first_name == "bar"
        assert user.last_name == "bar2"
        assert user.email == "email@example.com"

    @pytest.mark.django_db
    def test_patch_profile_missing_attrs(self, user: User, api_client: Client) -> None:
        data = {
            "first_name": "bar",
            "email": "email@example.com"
        }
        resp = api_client.patch(self._subject, data=data)
        assert resp.status_code == 200

        assert user.username == "user"
        assert user.first_name == "bar"
        assert user.last_name == ""
        assert user.email == "email@example.com"

    @pytest.mark.django_db
    def test_patch_profile_bad(self, user: User, api_client: Client) -> None:
        data = {
            "username": "user",
            "first_name": "",
            "last_name": "",
            "email": "not_an_email"
        }
        resp = api_client.patch(self._subject, data=data)
        assert resp.status_code == 400
        assert resp.json() == {
            'first_name': ['Expected at least 1 character'],
            'last_name': ['Expected at least 1 character'],
            'email': ['Enter a valid email address.'],
        }
