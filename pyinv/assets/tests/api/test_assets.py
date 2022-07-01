from django.test import TestCase
from rest_framework.test import APIClient

from assets.models import Asset, AssetModel, Manufacturer


class TestAssetAPI(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def add_asset(self) -> None:
        """Add an asset to the database."""
        self.manufacturer = Manufacturer.objects.create(name='Foo')
        self.model = AssetModel.objects.create(name="bar", manufacturer=self.manufacturer)
        self.asset = Asset.objects.create(asset_model=self.model)

    def add_asset_with_code(self) -> None:
        """Add an asset with a code to the database."""
        self.add_asset()
        self.asset.assetcode_set.create(code='12345')

    def test_list_no_assets(self) -> None:
        """Test that we get a valid response when there are no assets."""
        response = self.client.get('/api/v1/assets/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 0)
        self.assertEqual(data['next'], None)
        self.assertEqual(data['previous'], None)

    def test_list_one_asset(self) -> None:
        """Test that we get a valid response when there is one asset."""
        self.add_asset()

        response = self.client.get('/api/v1/assets/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['next'], None)
        self.assertEqual(data['previous'], None)

        asset = data['results'][0]
        self.assertEqual(asset['id'], str(self.asset.id))
        self.assertEqual(asset['asset_model']['slug'], self.model.slug)
        self.assertIsNone(asset['node'])
        self.assertEqual(asset['extra_data'], {})

        # It should have the UUID as the only asset code
        self.assertEqual(asset['asset_codes'], [str(self.asset.id)])

    def test_get_asset(self) -> None:
        """Test that we can fetch an individual asset."""
        self.add_asset()

        response = self.client.get(f'/api/v1/assets/{self.asset.id}/')
        self.assertEqual(response.status_code, 200)

        asset = response.json()
        self.assertEqual(asset['id'], str(self.asset.id))
        self.assertEqual(asset['asset_model']['slug'], self.model.slug)
        self.assertIsNone(asset['node'])
        self.assertEqual(asset['extra_data'], {})

        # It should have the UUID as the only asset code
        self.assertEqual(asset['asset_codes'], [str(self.asset.id)])

    def test_get_asset_by_code(self) -> None:
        """Test that we can fetch an asset by code."""
        self.add_asset_with_code()

        response = self.client.get('/api/v1/assets/?asset_code=12345')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['count'], 1)

        asset = data['results'][0]
        self.assertEqual(asset['asset_codes'], [str(self.asset.id), '12345'])
