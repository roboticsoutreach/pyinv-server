import pytest
from django.contrib.auth.models import User

from assets.models import Asset, AssetModel, Manufacturer, Node
from assets.tests.api.client import TestClient


@pytest.fixture
def user() -> User:
    return User.objects.create(username="user")


@pytest.fixture
def api_client() -> TestClient:
    return TestClient()


@pytest.fixture()
def user_client(user: User, api_client: TestClient) -> TestClient:
    api_client.force_authenticate(user)
    return api_client


@pytest.fixture
def manufacturer() -> Manufacturer:
    return Manufacturer.objects.create(name="Foo")


@pytest.fixture
def manufacturer_alt() -> Manufacturer:
    return Manufacturer.objects.create(name="Bar", slug="wasps")


@pytest.fixture
def asset_model(manufacturer: Manufacturer) -> AssetModel:
    return AssetModel.objects.create(name="Foo Model", manufacturer=manufacturer)


@pytest.fixture
def container_model(manufacturer_alt: Manufacturer) -> AssetModel:
    return AssetModel.objects.create(name="Bar Model", manufacturer=manufacturer_alt, is_container=True)


@pytest.fixture
def asset(asset_model: AssetModel) -> Asset:
    return Asset.objects.create(asset_model=asset_model)


@pytest.fixture
def container(container_model: AssetModel) -> Asset:
    return Asset.objects.create(asset_model=container_model)


@pytest.fixture
def container_with_child(asset_model: AssetModel, container_model: AssetModel) -> Asset:
    asset = Asset.objects.create(asset_model=asset_model)
    container = Asset.objects.create(asset_model=container_model)
    container_node = Node(node_type="A", asset=container)
    Node.add_root(instance=container_node)
    container_node.refresh_from_db()
    container_node.add_child(node_type="A", asset=asset)
    return container
