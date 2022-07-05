from typing import Any, Dict, Optional

import pytest
from django.contrib.auth.models import User

from assets.models import AssetModel, Manufacturer
from assets.tests.api.client import TestClient

from .base import APITestCase


class AssetModelTestCase(APITestCase):

    def assert_like_asset_model(self, data: Dict[str, Any]) -> None:
        assert data.keys() == {
            'name', 'slug', 'manufacturer', 'manufacturer_slug',
            'is_container', 'asset_count', 'created_at', 'updated_at',
        }
        assert isinstance(data["name"], str)
        assert isinstance(data["slug"], str)
        assert isinstance(data["is_container"], bool)
        assert isinstance(data["asset_count"], int)


@pytest.mark.django_db
class TestAssetModelListEndpoint(AssetModelTestCase):
    """Test the endpoint for listing, searching and sorting asset models."""

    def _subject(
        self,
        api_client: TestClient,
        *,
        expected_status: int = 200,
        params: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        response = api_client.get("/api/v1/asset-models/", params)
        assert response.status_code == expected_status
        return response.json()

    def test_no_results(self, api_client: TestClient) -> None:
        data = self._subject(api_client)
        assert data["count"] == 0
        assert data["next"] is None
        assert data["previous"] is None
        assert data["results"] == []

    def test_single_result(self, api_client: TestClient, asset_model: AssetModel) -> None:
        data = self._subject(api_client)
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        result = data["results"][0]
        self.assert_like_asset_model(result)
        assert result["name"] == asset_model.name
        assert result["slug"] == asset_model.slug

    @pytest.mark.usefixtures("asset_model", "container_model")
    def test_multiple_results_single_page(self, api_client: TestClient) -> None:
        data = self._subject(api_client)
        assert data["count"] == 2
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 2

    @pytest.mark.usefixtures("asset_model", "container_model")
    def test_multiple_results_multiple_pages(self, api_client: TestClient) -> None:
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

    @pytest.mark.usefixtures("asset_model", "container_model")
    def test_search_by_name(self, api_client: TestClient) -> None:
        data = self._subject(api_client, params={"search": "foo model"})
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        assert data["results"][0]["name"] == "Foo Model"

    @pytest.mark.usefixtures("asset_model", "container_model")
    def test_search_by_manufacturer(self, api_client: TestClient) -> None:
        data = self._subject(api_client, params={"search": "wasps"})
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        assert data["results"][0]["name"] == "Bar Model"

    @pytest.mark.usefixtures("asset_model", "container_model")
    def test_search_by_name_no_results(self, api_client: TestClient) -> None:
        data = self._subject(api_client, params={"search": "bees"})
        assert data["count"] == 0
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 0

    @pytest.mark.usefixtures("asset_model", "container_model")
    def test_order_by_name_asc(self, api_client: TestClient) -> None:
        data = self._subject(api_client, params={"ordering": "name"})
        assert [d["name"] for d in data["results"]] == ["Bar Model", "Foo Model"]

    @pytest.mark.usefixtures("asset_model", "container_model")
    def test_order_by_name_desc(self, api_client: TestClient) -> None:
        data = self._subject(api_client, params={"ordering": "-name"})
        assert [d["name"] for d in data["results"]] == ["Foo Model", "Bar Model"]


@pytest.mark.django_db
class TestAssetModelPostEndpoint(AssetModelTestCase):

    _subject = "/api/v1/asset-models/"
    _permission = "add_assetmodel"

    def test_post_no_auth(self, api_client: TestClient) -> None:
        resp = api_client.post(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_post_no_perms(self, user_client: TestClient) -> None:
        resp = user_client.post(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'You do not have permission to perform this action.'}

    def test_post_missing_fields(self, user_client: TestClient, user: User) -> None:
        self._set_permission(user)
        resp = user_client.post(self._subject)
        assert resp.status_code == 400
        assert resp.json() == {'name': ['This field is required.'], 'manufacturer_slug': ['This field is required.']}

    def test_post(self, user_client: TestClient, user: User, manufacturer: Manufacturer) -> None:
        data = {"name": "Bar", "slug": "bar", "is_container": True, "manufacturer_slug": manufacturer.slug}
        self._set_permission(user)
        resp = user_client.post(self._subject, data)
        assert resp.status_code == 201
        self.assert_like_asset_model(resp.json())

    def test_post_defaults(self, user_client: TestClient, user: User, manufacturer: Manufacturer) -> None:
        data = data = {"name": "Bar", "manufacturer_slug": manufacturer.slug}
        self._set_permission(user)
        resp = user_client.post(self._subject, data)
        assert resp.status_code == 201
        self.assert_like_asset_model(resp.json())

    def test_post_bad_slug(self, user_client: TestClient, user: User, manufacturer: Manufacturer) -> None:
        data = {"name": "Bar", "slug": "Not a Slug!!", "manufacturer_slug": manufacturer.slug}
        self._set_permission(user)
        resp = user_client.post(self._subject, data)
        assert resp.status_code == 201
        self.assert_like_asset_model(resp.json())
        assert resp.json()["slug"] == "not-a-slug"


@pytest.mark.django_db
class TestAssetModelGetIndividualEndpoint(AssetModelTestCase):

    _subject = "/api/v1/asset-models"

    def test_fetch_not_exists(self, api_client: TestClient) -> None:
        resp = api_client.get(f"{self._subject}/foo/")
        assert resp.status_code == 404
        assert resp.json() == {'detail': 'Not found.'}

    def test_fetch_manufacturer(self, api_client: TestClient, asset_model: AssetModel) -> None:
        resp = api_client.get(f"{self._subject}/foo-model/")
        assert resp.status_code == 200

        result = resp.json()
        self.assert_like_asset_model(result)
        assert result["name"] == asset_model.name


@pytest.mark.django_db
@pytest.mark.usefixtures("asset_model")
class TestAssetModelPutIndividualEndpoint(AssetModelTestCase):

    _subject = "/api/v1/asset-models/foo-model/"
    _permission = "change_assetmodel"

    def test_put_asset_model(self, user_client: TestClient, user: User) -> None:
        self._set_permission(user)
        resp = user_client.put(self._subject, {"name": "Yeet", "manufacturer_slug": "foo"})
        assert resp.status_code == 200
        assert AssetModel.objects.filter(name="Yeet").exists()
        self.assert_like_asset_model(resp.json())

    def test_put_asset_model_missing_field(self, user_client: TestClient, user: User) -> None:
        self._set_permission(user)
        resp = user_client.put(self._subject, {"name": "Yeet"})
        assert resp.status_code == 400
        assert resp.json() == {'manufacturer_slug': ['This field is required.']}

    def test_put_asset_model_no_auth(self, api_client: TestClient) -> None:
        resp = api_client.put(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_put_asset_model_no_permissions(self, user_client: TestClient) -> None:
        resp = user_client.put(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'You do not have permission to perform this action.'}


@pytest.mark.django_db
@pytest.mark.usefixtures("asset_model")
class TestAssetModelPatchIndividualEndpoint(AssetModelTestCase):

    _subject = "/api/v1/asset-models/foo-model/"
    _permission = "change_assetmodel"

    def test_patch_asset_model(self, user_client: TestClient, user: User) -> None:
        self._set_permission(user)
        resp = user_client.patch(self._subject, {"name": "Yeet", "manufacturer_slug": "foo"})
        assert resp.status_code == 200
        assert AssetModel.objects.filter(name="Yeet").exists()
        self.assert_like_asset_model(resp.json())

    def test_patch_asset_model_missing_field(self, user_client: TestClient, user: User) -> None:
        self._set_permission(user)
        resp = user_client.patch(self._subject, {"name": "Yeet"})
        assert resp.status_code == 200
        self.assert_like_asset_model(resp.json())

    def test_patch_asset_model_no_auth(self, api_client: TestClient) -> None:
        resp = api_client.patch(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_patch_asset_model_no_permissions(self, user_client: TestClient) -> None:
        resp = user_client.patch(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'You do not have permission to perform this action.'}


@pytest.mark.django_db
@pytest.mark.usefixtures("container_with_child")
class TestAssetModelCannotChangeContainerStateIfInvalid(AssetModelTestCase):

    _subject = "/api/v1/asset-models/bar-model/"
    _permission = "change_assetmodel"

    def test_put_container_to_not(self, user_client: TestClient, user: User) -> None:
        self._set_permission(user)
        resp = user_client.put(self._subject, {"name": "foo", "manufacturer_slug": "foo", "is_container": False})
        assert resp.status_code == 400
        assert resp.json() == {'detail': 'Unable to change asset model from a container, as some assets of this type contain items.'}  # noqa: E501

    def test_put_container_to_container(self, user_client: TestClient, user: User) -> None:
        self._set_permission(user)
        resp = user_client.put(self._subject, {"name": "foo", "manufacturer_slug": "foo", "is_container": True})
        assert resp.status_code == 200
        self.assert_like_asset_model(resp.json())

    def test_patch_container_to_not(self, user_client: TestClient, user: User) -> None:
        self._set_permission(user)
        resp = user_client.patch(self._subject, {"is_container": False})
        assert resp.status_code == 400
        assert resp.json() == {'detail': 'Unable to change asset model from a container, as some assets of this type contain items.'}  # noqa: E501

    def test_patch_container_to_container(self, user_client: TestClient, user: User) -> None:
        self._set_permission(user)
        resp = user_client.patch(self._subject, {"is_container": True})
        assert resp.status_code == 200
        self.assert_like_asset_model(resp.json())


@pytest.mark.django_db
@pytest.mark.usefixtures("asset_model")
class TestAssetModelDeleteIndividualEndpoint(AssetModelTestCase):

    _subject = "/api/v1/asset-models/foo-model/"
    _permission = "delete_assetmodel"

    def test_delete_asset_model(self, user_client: TestClient, user: User) -> None:
        self._set_permission(user)
        resp = user_client.delete(self._subject)
        assert resp.status_code == 204
        assert resp.content == b""
        assert not AssetModel.objects.filter(slug="foo-model").exists()

    @pytest.mark.usefixtures("asset")
    def test_delete_asset_model_with_asset(self, user_client: TestClient, user: User) -> None:
        self._set_permission(user)
        resp = user_client.delete(self._subject)
        assert resp.status_code == 400
        assert resp.json() == {'detail': 'Unable to delete object because it is referenced by other objects.'}

    def test_delete_asset_model_no_auth(self, api_client: TestClient) -> None:
        resp = api_client.delete(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_delete_asset_model_no_permissions(self, user_client: TestClient) -> None:
        resp = user_client.delete(self._subject)
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'You do not have permission to perform this action.'}
