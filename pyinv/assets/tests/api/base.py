from typing import Any, Dict
from uuid import UUID

from django.contrib.auth.models import Permission, User
from django.utils import dateparse


class PermissionsMixin:

    _permission: str

    def _get_permission(self) -> Permission:
        return Permission.objects.get(codename=self._permission)

    def _set_permission(self, user: User) -> None:
        user.user_permissions.add(self._get_permission())


class APITestCase(PermissionsMixin):

    def assert_like_asset(self, data: Dict[str, Any]) -> None:
        assert data.keys() == {
            'id', 'display_name', 'asset_model', 'asset_codes', 'first_asset_code',
            'created_at', 'updated_at', 'extra_data',
        }
        assert UUID(data["id"])
        assert isinstance(data["display_name"], str)
        self.assert_like_asset_model_link(data["asset_model"])
        assert isinstance(data["first_asset_code"], str)
        assert isinstance(data["asset_codes"], list)
        self.assert_valid_timestamps(data)
        assert isinstance(data["extra_data"], dict)

    def assert_like_asset_with_node(self, data: Dict[str, Any]) -> None:
        assert data.keys() == {
            'id', 'display_name', 'asset_model', 'asset_codes', 'first_asset_code',
            'created_at', 'updated_at', 'extra_data', 'node',
        }
        assert UUID(data["id"])
        assert isinstance(data["display_name"], str)
        self.assert_like_asset_model_link(data["asset_model"])
        assert isinstance(data["first_asset_code"], str)
        assert isinstance(data["asset_codes"], list)
        self.assert_valid_timestamps(data)
        assert isinstance(data["extra_data"], dict)
        if data["node"]:
            self.assert_like_node(data["node"])

    def assert_like_asset_model_link(self, data: Dict[str, Any]) -> None:
        assert data.keys() == {'name', 'slug'}
        assert isinstance(data["name"], str)
        assert isinstance(data["slug"], str)

    def assert_like_asset_model(self, data: Dict[str, Any]) -> None:
        assert data.keys() == {
            'name', 'slug', 'manufacturer', 'manufacturer_slug',
            'is_container', 'asset_count', 'created_at', 'updated_at',
        }
        assert isinstance(data["name"], str)
        assert isinstance(data["slug"], str)
        self.assert_like_manufacturer_link(data["manufacturer"])
        assert isinstance(data["manufacturer_slug"], str)
        assert isinstance(data["is_container"], bool)
        assert isinstance(data["asset_count"], int)
        self.assert_valid_timestamps(data)

    def assert_like_manufacturer_link(self, data: Dict[str, Any]) -> None:
        assert data.keys() == {"name", "slug"}
        assert isinstance(data["name"], str)
        assert isinstance(data["slug"], str)

    def assert_like_manufacturer(self, data: Dict[str, Any]) -> None:
        assert data.keys() == {"name", "slug", "updated_at", "created_at"}
        assert isinstance(data["name"], str)
        assert isinstance(data["slug"], str)
        self.assert_valid_timestamps(data)

    def assert_like_node_link(self, data: Dict[str, Any]) -> None:
        assert data.keys() == {'id', 'display_name', 'node_type', 'numchild', 'is_container'}

    def assert_like_node(self, data: Dict[str, Any]) -> None:
        assert data.keys() == {
            'id', 'display_name', 'node_type', 'numchild',
            'is_container', 'name', 'asset', 'depth', 'ancestors',
        }
        assert UUID(data["id"])
        assert isinstance(data["display_name"], str)
        assert data["node_type"] in ["A", "L"]
        assert isinstance(data["is_container"], bool)
        assert isinstance(data["numchild"], int)
        assert isinstance(data["depth"], int)
        assert isinstance(data["ancestors"], list)

        if data["asset"]:
            self.assert_like_asset(data["asset"])

        if data["ancestors"]:
            for ancestor in data["ancestors"]:
                self.assert_like_node_link(ancestor)

        # Sanity checks
        assert data["asset"] or data["node_type"] == "L"
        assert data["node_type"] == "A" or data["name"]
        assert data["node_type"] == "A" or data["display_name"] == data["name"]
        assert data["numchild"] == 0 or data["is_container"]
        assert data["depth"] - 1 == len(data["ancestors"])

    def assert_valid_timestamps(self, data: Dict[str, Any]) -> None:
        assert dateparse.parse_datetime(data["updated_at"]) is not None
        assert dateparse.parse_datetime(data["created_at"]) is not None
