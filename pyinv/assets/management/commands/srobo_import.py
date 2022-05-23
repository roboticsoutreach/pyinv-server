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

    def get_location(self, ref: str, create_if_not_exists: bool = True) -> Location:
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

    def _check_empty_location(self, location: Location) -> None:
        """
        Check if the location is empty.

        If it is, delete it!
        """
        # We need to check for None here, in case it was previously deleted in a cleanup.
        if location and location.contents.count() == 0 and location.children_set.count() == 0:
            self.stdout.write(f"Deleting {location}")
            location.delete()
            self._check_empty_location(location.parent)

    def handle(self, *args, **options):
        data_folder: Path = options['data_folder']
        self.stdout.write(f"Importing from {data_folder}")

        self._default_manufacturer, _ = Manufacturer.objects.get_or_create(name="Unknown")

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
                    self._handle_add_asset_event(cs, event)
                elif event["event"] == "move":
                    self._handle_move_asset_event(cs, event)

    def _handle_move_asset_event(self, cs, event) -> None:
        asset = Asset.get_by_code(event["asset_code"])
        new_location = self.get_location(event["new_location"])
        if asset is not None:
            try:
                ll = asset.linked_location
                ll.parent = new_location
                ll.save()
            except Asset.linked_location.RelatedObjectDoesNotExist:
                pass

            asset.location = new_location
            asset.save()

            # Fetch the old location after the tree has updated.
            old_location = self.get_location(event["old_location"])
            self._check_empty_location(old_location)

            AssetEvent.objects.create(
                changeset=cs,
                event_type="M",
                asset=asset,
                data=event,
            )
        else:
            self.stderr.write("Unable to find asset for move event")

    def _handle_add_asset_event(self, cs, event) -> None:
        asset_data = event["asset"]

        location = self.get_location(asset_data["location"])
        asset_model, _ = AssetModel.objects.get_or_create(
            name=asset_data["asset_type"],
            manufacturer=self._default_manufacturer,
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
            print("WARNING: You have run the import multiple times!")

        AssetEvent.objects.create(
            changeset=cs,
            event_type="A",
            asset=asset,
            data=event,
        )
