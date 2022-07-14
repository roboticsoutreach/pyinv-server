from typing import Any, Dict, Optional
from uuid import UUID

import pytest

from assets.models import ChangeSet
from pyinv.tests.client import Client

from .base import APITestCase


@pytest.mark.django_db
class TestChangesetListEndpoint(APITestCase):
    """Test the endpoint for listing, searching and sorting changesets."""

    def _subject(
        self,
        api_client: Client,
        *,
        expected_status: int = 200,
        params: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        response = api_client.get("/api/v1/changesets/", params)
        assert response.status_code == expected_status
        return response.json()

    def test_no_auth(self, api_client: Client) -> None:
        data = self._subject(api_client, expected_status=403)
        assert data == {'detail': 'Authentication credentials were not provided.'}

    def test_no_results(self, user_client: Client) -> None:
        data = self._subject(user_client)
        assert data["count"] == 0
        assert data["next"] is None
        assert data["previous"] is None
        assert data["results"] == []

    @pytest.mark.usefixtures("changeset")
    def test_single_result(self, user_client: Client) -> None:
        data = self._subject(user_client)
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        result = data["results"][0]
        self.assert_like_changeset_with_count(result)

    @pytest.mark.usefixtures("changeset", "changeset2")
    def test_multiple_results_single_page(self, user_client: Client) -> None:
        data = self._subject(user_client)
        assert data["count"] == 2
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 2

    @pytest.mark.usefixtures("changeset", "changeset2")
    def test_multiple_results_multiple_pages(self, user_client: Client) -> None:
        data = self._subject(user_client, params={"limit": "1"})
        assert data["count"] == 2
        assert data["next"] is not None
        assert data["previous"] is None
        assert len(data["results"]) == 1

        data = self._subject(user_client, params={"limit": "1", "offset": "1"})
        assert data["count"] == 2
        assert data["next"] is None
        assert data["previous"] is not None
        assert len(data["results"]) == 1

    @pytest.mark.usefixtures("changeset", "changeset2")
    def test_search_by_changeset_comment(self, user_client: Client) -> None:
        data = self._subject(user_client, params={"search": "bees"})
        assert data["count"] == 1
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 1

    @pytest.mark.usefixtures("changeset", "changeset2")
    def test_search_by_changeset_comment_no_results(self, user_client: Client) -> None:
        data = self._subject(user_client, params={"search": "knees"})
        assert data["count"] == 0
        assert data["next"] is None
        assert data["previous"] is None
        assert len(data["results"]) == 0


@pytest.mark.django_db
class TestAssetEventGetIndividualEndpoint(APITestCase):

    _subject = "/api/v1/changesets"

    def test_fetch_no_auth(self, api_client: Client) -> None:
        resp = api_client.get(f"{self._subject}/foo/")
        assert resp.status_code == 403
        assert resp.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_fetch_not_exists(self, user_client: Client) -> None:
        resp = user_client.get(f"{self._subject}/foo/")
        assert resp.status_code == 404
        assert resp.json() == {'detail': 'Not found.'}

    def test_fetch_manufacturer(self, user_client: Client, changeset: ChangeSet) -> None:
        resp = user_client.get(f"{self._subject}/{changeset.id}/")
        assert resp.status_code == 200

        result = resp.json()
        self.assert_like_changeset_with_count(result)
        assert UUID(result["id"]) == changeset.id
