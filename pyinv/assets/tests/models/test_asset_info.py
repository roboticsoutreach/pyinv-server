from assets.models import Asset, AssetCode, AssetModel, Manufacturer, Node
from django.test import TestCase


class TestAsset(TestCase):

    def setUp(self) -> None:
        """Set up the test."""
        self.manufacturer = Manufacturer(name="foo")
        self.manufacturer.save()
        self.asset_model = AssetModel(name="bar", manufacturer=self.manufacturer)
        self.asset_model.save()

    def test_create_asset_with_minimum_data(self) -> None:
        """Test that we can create an asset info."""
        asset = Asset.objects.create(asset_model=self.asset_model)
        self.assertEqual(asset.asset_model, self.asset_model)

        # Check defaults
        self.assertIsNotNone(asset.id)
        self.assertEqual(asset.state, "K")
        self.assertEqual(asset.extra_data, {})

    def test_asset_first_asset_code(self) -> None:
        """Test that we can fetch the first asset code."""
        asset = Asset.objects.create(asset_model=self.asset_model)
        self.assertEqual(asset.first_asset_code, str(asset.id))

        code = AssetCode.objects.create(code_type="A", code="foo", asset=asset)
        self.assertEqual(asset.first_asset_code, code.code)

    def test_asset_get_asset_codes(self) -> None:
        """Test that we can get all asset codes."""
        asset = Asset.objects.create(asset_model=self.asset_model)
        self.assertEqual(asset.asset_codes, [str(asset.id)])

        code = AssetCode.objects.create(code_type="A", code="foo", asset=asset)
        self.assertEqual(asset.asset_codes, [str(asset.id), code.code])

    def test_asset_display_name(self) -> None:
        """Test the display name without a node."""
        asset = Asset.objects.create(asset_model=self.asset_model)
        self.assertEqual(asset.display_name, "foo bar")

    def test_asset_display_name_node(self) -> None:
        """Test the display name with an unnamed node."""
        asset = Asset.objects.create(asset_model=self.asset_model)
        node = Node.add_root(node_type="A", asset=asset)
        self.assertEqual(asset.node, node)
        self.assertEqual(asset.display_name, "foo bar")

    def test_asset_display_name_named_node(self) -> None:
        """Test the display name with a named node."""
        asset = Asset.objects.create(asset_model=self.asset_model)
        node = Node.add_root(node_type="A", name="bees", asset=asset)
        self.assertEqual(asset.node, node)
        self.assertEqual(asset.display_name, "bees")

    def test_str(self) -> None:
        """Test the string representation."""
        asset = Asset.objects.create(asset_model=self.asset_model)
        self.assertEqual(str(asset), f"foo bar ({asset.id})")
