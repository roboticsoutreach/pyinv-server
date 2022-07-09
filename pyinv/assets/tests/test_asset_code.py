import unittest

import pytest
from django.core.exceptions import ValidationError

from assets.asset_codes import (
    AssetCodeStrategy,
    Damm32AssetCodeStrategy,
    StudentRoboticsAssetCodeStrategy,
)


class TestDamm32AssetCode(unittest.TestCase):

    VALID_CODES = ['INV-DRE-XY2', 'INV-ZI3-T5X', 'INV-JRU-NXQ', 'INV-JGK-YT7', 'INV-NOZ-RDX', 'INV-IQB-6AR', 'INV-MI5-5SK', 'INV-KUD-LHR', 'INV-J47-G7V', 'INV-Q7A-6VK']  # noqa: E501
    INVALID_CODES = ['INV-DRE-XYZ', 'INV-IZ3-T5X', 'SOR-JRU-NX2', 'INVDDDD-JGK-YT7', 'INVOZ-RDX', 'INV-1QB-6AR', 'INV-MI5-SSK', 'INVKUD-LHR', 'INV-J47-V', 'INV-Q7A-6V']  # noqa: E501

    def setUp(self) -> None:
        self.strategy = Damm32AssetCodeStrategy()

    def test_generate_and_validate_asset_codes(self) -> None:
        for _ in range(100):
            code = self.strategy.generate_new_code() or "Failed to generate"
            self.strategy.validate(code)

    def test_validate_good_asset_codes(self) -> None:
        for code in self.VALID_CODES:
            self.strategy.validate(code)

    def test_validate_bad_asset_codes(self) -> None:
        for code in self.INVALID_CODES:
            with self.assertRaises(ValidationError):
                self.strategy.validate(code)


class TestStudentRoboticsAssetCodes():

    @pytest.fixture
    def strategy(self) -> AssetCodeStrategy:
        return StudentRoboticsAssetCodeStrategy()

    @pytest.mark.parametrize("code", ["sr2UT29", "1VBC"])
    def test_valid_code(self, code: str, strategy: AssetCodeStrategy) -> None:
        strategy.validate(code)

    @pytest.mark.parametrize("code", ["srZZZ", "sr~!:@"])
    def test_invalid_characters(self, code: str, strategy: AssetCodeStrategy) -> None:
        with pytest.raises(ValidationError, match="Invalid characters in code:"):
            strategy.validate(code)

    @pytest.mark.parametrize("code", ["sr2UT27", "sr1VBV"])
    def test_invalid_checkdigit(self, code: str, strategy: AssetCodeStrategy) -> None:
        with pytest.raises(ValidationError, match="The check digit was invalid."):
            strategy.validate(code)

    def test_generate(self, strategy: AssetCodeStrategy) -> None:
        assert strategy.generate_new_code() is None
