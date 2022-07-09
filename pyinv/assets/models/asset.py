"""Asset Information."""

from typing import List, Optional
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import IntegrityError, models, transaction

from assets.asset_codes import AssetCodeType

from .asset_code import AssetCode
from .asset_model import AssetModel


class Asset(models.Model):
    """Asset."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # noqa: A003
    asset_model = models.ForeignKey(AssetModel, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra_data = models.JSONField(default=dict, blank=True)

    @property
    def display_name(self) -> str:
        try:
            return self.node.name or str(f"{self.asset_model} ({self.first_asset_code})")
        except Asset.node.RelatedObjectDoesNotExist:
            return str(self.asset_model)

    @property
    def first_asset_code(self) -> str:
        """A usable asset code for the asset."""
        code = self.assetcode_set.first()
        if code is None:
            return str(self.id)
        else:
            return code.code

    @property
    def asset_codes(self) -> List[str]:
        """A list of all asset codes for the asset."""
        return [str(self.id)] + [code.code for code in self.assetcode_set.all()]

    def __str__(self) -> str:
        return f"{self.display_name} ({self.first_asset_code})"

    def add_asset_code(self, code_type: AssetCodeType, code: Optional[str]) -> AssetCode:
        """
        Add an asset code to an asset.

        :raises ValueError: Unable to generate code, or unrecognised code type.
        :raises django.db.IntegrityError: The specifed code already exists
        """
        strategy = AssetCodeType.get_strategy(code_type)
        if code:
            try:
                strategy.validate(code)
                return AssetCode.objects.create(asset=self, code=code, code_type=code_type.value)
            except ValidationError as e:
                raise ValueError(f"Provided asset code is not valid: {e}")

        # Generate and attempt to insert codes in a loop
        while True:
            try:
                if (code := strategy.generate_new_code()) is None:
                    raise ValueError("Unable to generate an asset code of that type.")

                with transaction.atomic():
                    return AssetCode.objects.create(asset=self, code=code, code_type=code_type.value)
            except IntegrityError:
                pass
