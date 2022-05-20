from json import loads
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
        parser.add_argument('data_folder', type=Path)

    def get_location(self, ref) -> Location:
        try:
            code = AssetCode.objects.get(code=ref)
            parent_asset = code.asset
            if not parent_asset.asset_model.is_container:
                parent_asset.asset_model.is_container = True
                parent_asset.asset_model.save()
            location, _ = Location.objects.get_or_create(parent=parent_asset.location, asset=parent_asset)
            return location
        except AssetCode.DoesNotExist:
            if ref.startswith("sr"):
                loc, _ = Location.objects.get_or_create(name="unknown")
                return loc
            else:
                parts = ref.split("/")
                return self.get_non_asset_location(parts)

    def get_non_asset_location(self, parts: List[str], parent=None) -> None:
        top_level = parts.pop(0)

        location, _ = Location.objects.get_or_create(name=top_level, parent=parent)

        if len(parts) > 0:
            return self.get_non_asset_location(parts, location)
        else:
            return location

    def handle(self, *args, **options):
        data_folder: Path = options['data_folder']
        self.stdout.write(f"Importing from {data_folder}")

        manufacturer, _ = Manufacturer.objects.get_or_create(name="Unknown")

        for file in sorted(data_folder.glob("*.yaml")):
            self.stdout.write(f"Processing {file}")
            data = loads(file.read_text())

            user, _ = User.objects.get_or_create(
                username=data['user'],
                email=data['user'],
                is_active=False,
            )

            cs = Changeset.objects.create(
                timestamp=dateparse.parse_datetime(data["timestamp"] + "Z"),
                user=user,
                comment=data["comment"],
            )

            for event in data["events"]:
                if event["event"] == "add":
                    asset_data = event["asset"]
                    print("Adding", asset_data)

                    location = self.get_location(asset_data["location"])
                    asset_model, _ = AssetModel.objects.get_or_create(
                        name=asset_data["asset_type"],
                        manufacturer=manufacturer,
                    )

                    asset = Asset.objects.create(
                        asset_model=asset_model,
                        state="K",
                        location=location,
                        extra_data=asset_data["data"],
                    )

                    try:
                        AssetCode.objects.get_or_create(asset=asset, code=asset_data["asset_code"], code_type="A")
                    except IntegrityError:
                        pass

                    AssetEvent.objects.create(
                        changeset=cs,
                        event_type="A",
                        asset=asset,
                        data=event,
                    )
