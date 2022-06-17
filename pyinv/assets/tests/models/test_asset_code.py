from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase

from assets.models import Asset, AssetCode, AssetModel, Manufacturer


class TestAssetCodeModel(TestCase):

    def setUp(self) -> None:
        """Set up the test."""
        self.manufacturer = Manufacturer(name="foo")
        self.manufacturer.save()
        self.asset_model = AssetModel(name="bar", manufacturer=self.manufacturer)
        self.asset_model.save()
        self.asset = Asset(asset_model=self.asset_model)
        self.asset.save()

    def test_no_duplicate_code(self) -> None:
        """Test that we can make a arbitrary asset code."""
        code = AssetCode(code_type="A", code="foo", asset=self.asset)
        code.save()
        code2 = AssetCode(code_type="A", code="foo", asset=self.asset)

        with self.assertRaises(IntegrityError):
            code2.save()

    def test_str_representation(self) -> None:
        """Test that we can make a arbitrary asset code."""
        code = AssetCode(code_type="A", code="foo", asset=self.asset)
        self.assertEqual(str(code), "foo")

    def test_arbitrary_code(self) -> None:
        """Test that we can make a arbitrary asset code."""
        code = AssetCode(code_type="A", code="foo", asset=self.asset)
        self.assertEqual(code.code, "foo")

    def test_arbitrary_code_too_short(self) -> None:
        """Test that we cannot make a zero length asset code."""
        code = AssetCode.objects.create(code_type="A", code="", asset=self.asset)
        with self.assertRaises(ValidationError):
            code.full_clean()

    def test_validate_damm32(self) -> None:
        """Test that we can create a valid damm32 code."""
        code = AssetCode(code_type="D", code="INV-ASE-SEJ", asset=self.asset)
        code.full_clean()

    def test_validate_damm32_bad_check_digit(self) -> None:
        """Test that we catch a bad check digit."""
        code = AssetCode(code_type="D", code="INV-ASE-SEU", asset=self.asset)
        with self.assertRaises(ValidationError):
            code.full_clean()

    def test_validate_damm32_bad_prefix(self) -> None:
        """Test that we catch a bad prefix."""
        code = AssetCode(code_type="D", code="ABC-DEF-GH6", asset=self.asset)
        with self.assertRaisesRegex(ValidationError, "Invalid asset code prefix"):
            code.full_clean()

    def test_invalid_damm32_format(self) -> None:
        """Test that we catch a bad damm32 format."""
        code = AssetCode(code_type="D", code="foo", asset=self.asset)
        with self.assertRaises(ValidationError):
            code.full_clean()

    def test_invalid_format(self) -> None:
        """Test that we catch a non-existent format."""
        code = AssetCode(code_type="?", code="foo", asset=self.asset)
        with self.assertRaises(ValueError):
            code.full_clean()
