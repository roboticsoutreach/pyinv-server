from json import loads
import json
from pathlib import Path
from typing import List

from assets.models import (
    Asset,
    AssetCode,
    AssetEvent,
    AssetModel,
    Changeset,
    Location,
    Manufacturer,
)
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils import dateparse


class Command(BaseCommand):

    help = 'Import assets from Student Robotics JSON format'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument('data_file', type=Path)

    def handle(self, *args, **options):
        data_file: Path = options['data_file']
        self.stdout.write(f"Importing from {data_file}")

        data = json.loads(data_file.read_text())

        self._default_manufacturer, _ = Manufacturer.objects.get_or_create(name="Unknown")

        # First Pass
        for ref, object in data.items():
            if object["type"] == "asset":
                self._add_asset(object["data"])
            elif object["type"] == "location":
                pass
            else:
                raise ValueError(f"Unknown object type {object['type']}")

        # Second Pass
        for asset in Asset.objects.all():
            asset.location = self.get_location(data, data[asset.first_asset_code]["data"]["location"])
            asset.state = "K"
            asset.save()


    def get_location(self, data, ref: str, create_if_not_exists: bool = True) -> Location:
        linked_asset = Asset.get_by_code(ref)
        if linked_asset is not None:
            # Check if the location already exists
            try:
                return linked_asset.linked_location
            except Asset.linked_location.RelatedObjectDoesNotExist:
                # Set the asset model to be a container if it is not already
                if not linked_asset.asset_model.is_container:
                    linked_asset.asset_model.is_container = True
                    linked_asset.asset_model.save()

                # Move the asset
                if linked_asset.location is None:
                    linked_asset.state = "K"
                    linked_asset.location = self.get_location(data, data[linked_asset.first_asset_code]["data"]["location"])
                    linked_asset.save()

                # Create the new location
                return Location.objects.create(
                    parent=linked_asset.location,
                    asset=linked_asset,
                )
        elif create_if_not_exists:
            if ref.startswith("sr"):
                self.stderr.write(f"Unknown linked_location reference: {ref}")
                loc, _ = Location.objects.get_or_create(name="unknown-ref-srobo-import")
                return loc
            else:
                parts = ref.split("/")
                return self.get_non_asset_location(parts)
        else:
            raise RuntimeError(f"Location {ref} does not exist!")

    def get_non_asset_location(self, parts: List[str], parent=None) -> None:
        top_level = parts.pop(0)

        location, _ = Location.objects.get_or_create(name=top_level, parent=parent)

        if len(parts) > 0:
            return self.get_non_asset_location(parts, location)
        else:
            return location

    def _add_asset(self, data) -> None:
        asset_model, _ = AssetModel.objects.get_or_create(
            name=data["asset_type"],
            manufacturer=self._default_manufacturer,
        )

        asset = Asset.objects.create(
            asset_model=asset_model,
            state="L",
            location=None,
            extra_data=data["data"],
        )

        try:
            AssetCode.objects.get_or_create(asset=asset, code=data["asset_code"], code_type="A")
        except IntegrityError:
            print("WARNING: You have run the import multiple times!")
