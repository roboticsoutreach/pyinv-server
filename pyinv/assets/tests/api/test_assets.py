from typing import Any, Dict, Optional, Union

import pytest

from assets.models import Asset
from pyinv.tests.client import Client

from .base import APITestCase


@pytest.mark.django_db
class TestAssetListEndpoint(APITestCase):
    """Test the endpoint for listing, searching and sorting assets."""

    def _subject(
        self,
        api_client: Client,
        *,
        expected_status: int = 200,
        params: Optional[Dict[str, Union[str, bool]]] = None,
    ) -> Dict[str, Any]:
        response = api_client.get("/api/v1/assets/", params)
        assert response.status_code == expected_status
        return response.json()

    def test_no_results(self, api_client: Client) -> None:
        data = self._subject(api_client)
        assert data["count"] == 0
        assert data["next"] is None
        assert data["previous"] is None
        assert data["results"] == []

    @pytest.mark.usefixtures("asset")
    def test_single_result(self, api_client: Client) -> None:
        data = self._subject(api_client)
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        result = data["results"][0]
        self.assert_like_asset_with_node(result)

    @pytest.mark.usefixtures("asset", "container")
    def test_multiple_results_single_page(self, api_client: Client) -> None:
        data = self._subject(api_client)
        assert data["count"] == 2
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 2

    @pytest.mark.usefixtures("asset", "container")
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

    @pytest.mark.usefixtures("container", "container_with_child")
    def test_filter_by_is_container(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"is_container": True})
        assert data["count"] == 2

        data = self._subject(api_client, params={"is_container": False})
        assert data["count"] == 1

    @pytest.mark.usefixtures("container", "container_with_child")
    def test_filter_by_has_node(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"has_node": True})
        assert data["count"] == 2

        data = self._subject(api_client, params={"has_node": False})
        assert data["count"] == 1

    @pytest.mark.usefixtures("asset_with_code", "container")
    def test_filter_by_asset_model(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"asset_model": "bar-model"})
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        assert data["results"][0]["display_name"].startswith("Bar Model")

    @pytest.mark.usefixtures("asset_with_code", "container")
    def test_find_by_asset_code(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"asset_code": "asset-code"})
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        assert data["results"][0]["display_name"].startswith("Foo Model")

    @pytest.mark.usefixtures("asset_with_code", "container")
    def test_find_by_asset_code_no_results(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"asset_code": "bees"})
        assert data["count"] == 0
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 0

    @pytest.mark.usefixtures("asset_with_code", "container")
    def test_search_by_asset_code(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"search": "asset-code"})
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        assert data["results"][0]["display_name"].startswith("Foo Model")

    @pytest.mark.usefixtures("asset_model", "container_model")
    def test_search_no_results(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"search": "bees"})
        assert data["count"] == 0
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 0

    @pytest.mark.usefixtures("asset_with_code", "container")
    def test_search_by_model(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"search": "foo"})
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        assert data["results"][0]["display_name"].startswith("Foo Model")

    @pytest.mark.usefixtures("named_container_with_child")
    def test_search_by_node_name(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"search": "node-name"})
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        assert data["results"][0]["display_name"] == "node-name"


@pytest.mark.django_db
class TestAssetGetIndividualEndpoint(APITestCase):

    _subject = "/api/v1/assets"

    def test_fetch_not_exists(self, api_client: Client) -> None:
        resp = api_client.get(f"{self._subject}/000/")
        assert resp.status_code == 404
        assert resp.json() == {'detail': 'Not found.'}

    def test_fetch(self, api_client: Client, asset: Asset) -> None:
        resp = api_client.get(f"{self._subject}/{asset.id}/")
        assert resp.status_code == 200

        result = resp.json()
        self.assert_like_asset_with_node(result)
