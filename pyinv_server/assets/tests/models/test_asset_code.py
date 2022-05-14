from assets.models import AssetCode
from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase


class TestAssetCodeModel(TestCase):

    def test_no_duplicate_code(self) -> None:
        """Test that we can make a arbitrary asset code."""
        code = AssetCode(code_type="A", code="foo")
        code.save()
        code2 = AssetCode(code_type="A", code="foo")

        with self.assertRaises(IntegrityError):
            code2.save()

    def test_arbitrary_code(self) -> None:
        """Test that we can make a arbitrary asset code."""
        code = AssetCode(code_type="A", code="foo")
        self.assertEqual(code.code, "foo")

    def test_validate_damm32(self) -> None:
        """Test that we can create a valid damm32 code."""
        code = AssetCode(code_type="D", code="INV-ASE-SEJ")
        code.full_clean()

    def test_validate_damm32_bad_check_digit(self) -> None:
        """Test that we catch a bad check digit."""
        code = AssetCode(code_type="D", code="INV-ASE-SEU")
        with self.assertRaises(ValidationError):
            code.full_clean()

    def test_invalid_damm32_format(self) -> None:
        """Test that we catch a bad damm32 format."""
        code = AssetCode(code_type="D", code="foo")
        with self.assertRaises(ValidationError):
            code.full_clean()

    def test_invalid_format(self) -> None:
        """Test that we catch a non-existent format."""
        code = AssetCode(code_type="?", code="foo")
        with self.assertRaises(ValueError):
            code.full_clean()
