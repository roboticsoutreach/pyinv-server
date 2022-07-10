from typing import Any, Dict, Optional, Union
from uuid import UUID

import pytest

from assets.models import Asset, Node
from pyinv.tests.client import Client

from .base import APITestCase


@pytest.mark.django_db
class TestNodeListEndpoint(APITestCase):
    """Test the endpoint for listing, searching and sorting nodes."""

    def _subject(
        self,
        api_client: Client,
        *,
        expected_status: int = 200,
        params: Optional[Dict[str, Union[str, bool, UUID]]] = None,
    ) -> Dict[str, Any]:
        response = api_client.get("/api/v1/nodes/", params)
        assert response.status_code == expected_status
        return response.json()

    def test_no_results(self, api_client: Client) -> None:
        data = self._subject(api_client)
        assert data["count"] == 0
        assert data["next"] is None
        assert data["previous"] is None
        assert data["results"] == []

    @pytest.mark.usefixtures("location")
    def test_single_result(self, api_client: Client) -> None:
        data = self._subject(api_client)
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        result = data["results"][0]
        self.assert_like_node(result)

    @pytest.mark.usefixtures("container_with_child")
    def test_multiple_results_single_page(self, api_client: Client) -> None:
        data = self._subject(api_client)
        assert data["count"] == 2
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 2

    @pytest.mark.usefixtures("container_with_child")
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

    @pytest.mark.usefixtures("container_with_child")
    def test_results_contain_tree_structure_as_expected(self, api_client: Client) -> None:
        data = self._subject(api_client)
        for n in data["results"]:
            self.assert_like_node(n)

    @pytest.mark.usefixtures("location", "container_with_child")
    def test_filter_by_is_container(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"is_container": True})
        assert data["count"] == 2

        data = self._subject(api_client, params={"is_container": False})
        assert data["count"] == 1

    @pytest.mark.usefixtures("location")
    def test_filter_by_parent(self, api_client: Client, location: Node, container_with_child: Asset) -> None:
        data = self._subject(api_client, params={"parent": "root"})
        assert data["count"] == 2

        data = self._subject(api_client, params={"parent": "not-a-node"})
        assert data["count"] == 0

        data = self._subject(api_client, params={"parent": location.id})
        assert data["count"] == 0

        data = self._subject(api_client, params={"parent": container_with_child.node.id})
        assert data["count"] == 1

    def test_filter_by_descendent_of(self, api_client: Client, location: Node, container_with_child: Asset) -> None:
        data = self._subject(api_client, params={"descendent_of": "root"})
        assert data["count"] == 3

        data = self._subject(api_client, params={"descendent_of": "not-a-node"})
        assert data["count"] == 0

        data = self._subject(api_client, params={"descendent_of": location.id})
        assert data["count"] == 0

        data = self._subject(api_client, params={"descendent_of": container_with_child.node.id})
        assert data["count"] == 1

    @pytest.mark.usefixtures("location", "container_with_child")
    def test_filter_by_node_type(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"node_type": "A"})
        assert data["count"] == 2

        data = self._subject(api_client, params={"node_type": "L"})
        assert data["count"] == 1

    @pytest.mark.usefixtures("location", "container_with_child")
    def test_search_no_results(self, api_client: Client) -> None:
        data = self._subject(api_client, params={"search": "bees"})
        assert data["count"] == 0
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 0


@pytest.mark.django_db
class TestAssetGetIndividualEndpoint(APITestCase):

    _subject = "/api/v1/nodes"

    def test_fetch_not_exists(self, api_client: Client) -> None:
        resp = api_client.get(f"{self._subject}/000/")
        assert resp.status_code == 404
        assert resp.json() == {'detail': 'Not found.'}

    def test_fetch(self, api_client: Client, location: Node) -> None:
        resp = api_client.get(f"{self._subject}/{location.id}/")
        assert resp.status_code == 200

        result = resp.json()
        self.assert_like_node(result)
