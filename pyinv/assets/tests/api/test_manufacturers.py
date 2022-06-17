from django.test import TestCase
from rest_framework.test import APIClient

from assets.models import Manufacturer


class TestManufacturerAPI(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def add_manufacturer(self) -> None:
        """Add an asset to the database."""
        self.manufacturer = Manufacturer.objects.create(name='Foo')

    def test_list_no_manufacturers(self) -> None:
        """Test that we get a valid response when there are no manufacturers."""
        response = self.client.get('/api/v1/manufacturers/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 0)
        self.assertEqual(data['next'], None)
        self.assertEqual(data['previous'], None)

    def test_list_one_manufacturer(self) -> None:
        """Test that we get a valid response when there is one manufacturer."""
        self.add_manufacturer()

        response = self.client.get('/api/v1/manufacturers/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['next'], None)
        self.assertEqual(data['previous'], None)

        asset = data['results'][0]
        self.assertEqual(asset['name'], "Foo")
        self.assertEqual(asset['slug'], 'foo')

    def test_get_manufacturer(self) -> None:
        """Test that we can fetch an individual manufacturer."""
        self.add_manufacturer()

        response = self.client.get('/api/v1/manufacturers/foo/')
        self.assertEqual(response.status_code, 200)

        asset = response.json()
        self.assertEqual(asset['name'], "Foo")
        self.assertEqual(asset['slug'], 'foo')
