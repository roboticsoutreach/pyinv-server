import pytest
from django.db import IntegrityError
from django.test import TestCase

from assets.asset_codes import AssetCodeType
from assets.models import Asset, AssetCode, AssetModel, Manufacturer, Node


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
        self.assertEqual(asset.display_name, "bar")

    def test_asset_display_name_node(self) -> None:
        """Test the display name with an unnamed node."""
        asset = Asset.objects.create(asset_model=self.asset_model)
        node = Node.add_root(node_type="A", asset=asset)
        self.assertEqual(asset.node, node)
        self.assertEqual(asset.display_name, f"bar ({asset.first_asset_code})")

    def test_asset_display_name_named_node(self) -> None:
        """Test the display name with a named node."""
        asset = Asset.objects.create(asset_model=self.asset_model)
        node = Node.add_root(node_type="A", name="bees", asset=asset)
        self.assertEqual(asset.node, node)
        self.assertEqual(asset.display_name, "bees")

    def test_str(self) -> None:
        """Test the string representation."""
        asset = Asset.objects.create(asset_model=self.asset_model)
        self.assertEqual(str(asset), f"bar ({asset.id})")


@pytest.mark.django_db
class TestAssetCodeGeneration:
    """Test the Asset.add_asset_code function."""

    def test_assign_asset_code(self, asset: Asset) -> None:
        assert "ABC" not in asset.asset_codes
        asset.add_asset_code(AssetCodeType.ARBITRARY, "ABC")
        assert "ABC" in asset.asset_codes

    def test_assign_duplicate_code(self, asset: Asset, container: Asset) -> None:
        asset.add_asset_code(AssetCodeType.ARBITRARY, "ABC")

        with pytest.raises(IntegrityError, match="UNIQUE constraint failed: assets_assetcode.code"):
            container.add_asset_code(AssetCodeType.ARBITRARY, "ABC")

    def test_generate_asset_code(self, asset: Asset) -> None:
        code = asset.add_asset_code(AssetCodeType.DAMM32, None)
        assert code.code in asset.asset_codes

    def test_unable_to_generate_asset_code(self, asset: Asset) -> None:
        with pytest.raises(ValueError, match="Unable to generate an asset code of that type."):
            asset.add_asset_code(AssetCodeType.SROBO, None)

    def test_bad_provided_code(self, asset: Asset) -> None:
        with pytest.raises(
            ValueError,
            match=r"Provided asset code is not valid: \['The check digit was invalid.'\]",
        ):
            asset.add_asset_code(AssetCodeType.SROBO, "srABCABC")
