from assets.models import Manufacturer
from django.test import TestCase


class TestManufacturerModel(TestCase):

    def setUp(self):
        super().setUp()
        self.bees = Manufacturer.objects.create(name="Bees")

    def test_manufacturer_set_slug_automatically(self) -> None:
        """Test that the slug is set automatically."""
        self.assertEqual(self.bees.slug, "bees")

    def test_manufacturer_read_notes(self) -> None:
        """Test that we can read the notes field."""
        bees = Manufacturer.objects.get(name="Bees")
        self.assertEqual(bees.notes, "")

    def test_str(self) -> None:
        self.assertEqual(str(self.bees), "Bees")