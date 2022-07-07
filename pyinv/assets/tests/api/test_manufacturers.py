from typing import Any, Dict, Optional

import pytest
from django.contrib.auth.models import User

from assets.models import Manufacturer
from assets.tests.api.client import Client

from .base import APITestCase


@pytest.mark.django_db
class TestManufacturerListEndpoint(APITestCase):
    """Test the endpoint for listing, searching and sorting manufacturers."""

    def _subject(
        self,
        api_client: Client,
        *,
        expected_status: int = 200,
        params: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        response = api_client.get("/api/v1/manufacturers/", params)
        assert response.status_code == expected_status
        return response.json()

    def test_no_results(self, api_client: Client) -> None:
        data = self._subject(api_client)
        assert data["count"] == 0
        assert data["next"] is None
        assert data["previous"] is None
        assert data["results"] == []

    def test_single_result(self, api_client: Client, manufacturer: Manufacturer) -> None:
        data = self._subject(api_client)
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        result = data["results"][0]
        self.assert_like_manufacturer(result)
        assert result["name"] == manufacturer.name
        assert result["slug"] == manufacturer.slug

    @pytest.mark.usefixtures("manufacturer", "manufacturer_alt")
    def test_multiple_results_single_page(self, api_client: Client) -> None:
        data = self._subject(api_client)
        assert data["count"] == 2
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 2

    @pytest.mark.usefixtures("manufacturer", "manufacturer_alt")
    def test_multiple_results_multiple_pages(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"limit": "1"})
        assert data["count"] == 2
        assert data["next"] is not None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        data = self._subject(api_client, params={"limit": "1", "offset": "1"})
        assert data["count"] == 2
        assert data["next"] is None
        assert data["previous"] is not None
        assert len(data["results"]) == 1

    @pytest.mark.usefixtures("manufacturer", "manufacturer_alt")
    def test_search_by_name(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"search": "foo"})
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        assert data["results"][0]["name"] == "Foo"

    @pytest.mark.usefixtures("manufacturer", "manufacturer_alt")
    def test_search_by_name_no_results(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"search": "bees"})
        assert data["count"] == 0
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 0

    @pytest.mark.usefixtures("manufacturer", "manufacturer_alt")
    def test_order_by_name_asc(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"ordering": "name"})
        assert [d["name"] for d in data["results"]] == ["Bar", "Foo"]

    @pytest.mark.usefixtures("manufacturer", "manufacturer_alt")
    def test_order_by_name_desc(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"ordering": "-name"})
        assert [d["name"] for d in data["results"]] == ["Foo", "Bar"]

    @pytest.mark.usefixtures("manufacturer", "manufacturer_alt")
    def test_order_by_slug_asc(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"ordering": "slug"})
        assert [d["name"] for d in data["results"]] == ["Foo", "Bar"]

    @pytest.mark.usefixtures("manufacturer", "manufacturer_alt")
    def test_order_by_slug_desc(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"ordering": "-slug"})
        assert [d["name"] for d in data["results"]] == ["Bar", "Foo"]


@pytest.mark.django_db
class TestManufacturerPostEndpoint(APITestCase):

    _subject = "/api/v1/manufacturers/"
    _permission = "add_manufacturer"

    def test_post_no_auth(self, api_client: Client) -> None:
        resp = api_client.post(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_post_no_perms(self, user_client: Client) -> None:
        resp = user_client.post(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'You do not have permission to perform this action.'}

    def test_post_missing_fields(self, user_client: Client, user: User) -> None:
        self._set_permission(user)
        resp = user_client.post(self._subject)
        assert resp.status_code == 400
        assert resp.json() == {'name': ['This field is required.']}

    def test_post(self, user_client: Client, user: User) -> None:
        data = {"name": "Bar", "slug": "bar"}
        self._set_permission(user)
        resp = user_client.post(self._subject, data)
        assert resp.status_code == 201
        self.assert_like_manufacturer(resp.json())

    def test_post_default_slug(self, user_client: Client, user: User) -> None:
        data = {"name": "Bar"}
        self._set_permission(user)
        resp = user_client.post(self._subject, data)
        assert resp.status_code == 201
        self.assert_like_manufacturer(resp.json())

    def test_post_bad_slug(self, user_client: Client, user: User) -> None:
        data = {"name": "Bar", "slug": "Not a Slug!!"}
        self._set_permission(user)
        resp = user_client.post(self._subject, data)
        assert resp.status_code == 201
        self.assert_like_manufacturer(resp.json())
        assert resp.json()["slug"] == "not-a-slug"

    @pytest.mark.usefixtures("manufacturer")
    def test_post_duplicate_slug(self, user_client: Client, user: User) -> None:
        data = {"name": "Bees", "slug": "foo"}
        self._set_permission(user)
        resp = user_client.post(self._subject, data)
        assert resp.status_code == 201
        self.assert_like_manufacturer(resp.json())
        assert resp.json()["slug"] == "foo-2"


@pytest.mark.django_db
class TestManufacturerGetIndividualEndpoint(APITestCase):

    _subject = "/api/v1/manufacturers"

    def test_fetch_not_exists(self, api_client: Client) -> None:
        resp = api_client.get(f"{self._subject}/foo/")
        assert resp.status_code == 404
        assert resp.json() == {'detail': 'Not found.'}

    def test_fetch_manufacturer(self, api_client: Client, manufacturer: Manufacturer) -> None:
        resp = api_client.get(f"{self._subject}/foo/")
        assert resp.status_code == 200

        result = resp.json()
        assert result.keys() == {"name", "slug", "updated_at", "created_at"}
        assert result["name"] == manufacturer.name
        assert result["slug"] == manufacturer.slug


@pytest.mark.django_db
@pytest.mark.usefixtures("manufacturer")
class TestManufacturerPutIndividualEndpoint(APITestCase):

    _subject = "/api/v1/manufacturers/foo/"
    _permission = "change_manufacturer"

    def test_put_manufacturer(self, user_client: Client, user: User) -> None:
        self._set_permission(user)
        resp = user_client.put(self._subject, {"name": "Yeet"})
        assert resp.status_code == 200
        assert Manufacturer.objects.filter(name="Yeet").exists()
        self.assert_like_manufacturer(resp.json())

    def test_put_manufacturer_no_auth(self, api_client: Client) -> None:
        resp = api_client.put(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_put_manufacturer_no_permissions(self, user_client: Client) -> None:
        resp = user_client.put(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'You do not have permission to perform this action.'}

    def test_put_manufacturer_timestamps(self, user_client: Client, user: User) -> None:
        self._set_permission(user)
        resp = user_client.put(self._subject, {"updated_at": "Yeet"})
        assert resp.status_code == 400
        assert resp.json() == {'name': ['This field is required.']}


@pytest.mark.django_db
@pytest.mark.usefixtures("manufacturer")
class TestManufacturerPatchIndividualEndpoint(APITestCase):

    _subject = "/api/v1/manufacturers/foo/"
    _permission = "change_manufacturer"

    def test_patch_manufacturer(self, user_client: Client, user: User) -> None:
        self._set_permission(user)
        resp = user_client.patch(self._subject, {"name": "Yeet"})
        assert resp.status_code == 200
        assert Manufacturer.objects.filter(name="Yeet").exists()
        self.assert_like_manufacturer(resp.json())

    def test_patch_manufacturer_no_auth(self, api_client: Client) -> None:
        resp = api_client.patch(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_patch_manufacturer_no_permissions(self, user_client: Client) -> None:
        resp = user_client.patch(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'You do not have permission to perform this action.'}

    def test_patch_manufacturer_timestamps(self, user_client: Client, user: User) -> None:
        self._set_permission(user)
        resp = user_client.patch(self._subject, {"updated_at": "Yeet"})
        assert resp.status_code == 200
        self.assert_like_manufacturer(resp.json())


@pytest.mark.django_db
@pytest.mark.usefixtures("manufacturer")
class TestManufacturerDeleteIndividualEndpoint(APITestCase):

    _subject = "/api/v1/manufacturers/foo/"
    _permission = "delete_manufacturer"

    def test_delete_manufacturer(self, user_client: Client, user: User) -> None:
        self._set_permission(user)
        resp = user_client.delete(self._subject)
        assert resp.status_code == 204
        assert resp.content == b""
        assert not Manufacturer.objects.filter(slug="foo").exists()

    @pytest.mark.usefixtures("asset_model")
    def test_delete_manufacturer_with_model(self, user_client: Client, user: User) -> None:
        self._set_permission(user)
        resp = user_client.delete(self._subject)
        assert resp.status_code == 400
        assert resp.json() == {'detail': 'Unable to delete object because it is referenced by other objects.'}

    def test_delete_manufacturer_no_auth(self, api_client: Client) -> None:
        resp = api_client.delete(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_delete_manufacturer_no_permissions(self, user_client: Client) -> None:
        resp = user_client.delete(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'You do not have permission to perform this action.'}
