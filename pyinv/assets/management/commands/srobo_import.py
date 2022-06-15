import json
from pathlib import Path

from assets.models import Asset, AssetCode, AssetModel, Manufacturer, Node
from django.core.management.base import BaseCommand
from django.db import IntegrityError


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
        for obj in data.values():
            if obj["type"] == "asset":
                pass
                self._add_asset(obj["data"])
            elif obj["type"] == "location":
                Node.add_root(instance=Node(node_type="L", name=obj["data"][0]))
            else:
                raise ValueError(f"Unknown object type {obj['type']}")

        # Second Pass
        for obj in data.values():
            if obj["type"] == "asset":
                pass
            elif obj["type"] == "location":
                node = Node.objects.get(name=obj["data"][0], node_type="L")
                if obj["data"][1] != ".":
                    parent = Node.objects.get(name=obj["data"][1], node_type="L")
                    node.move(parent, pos="last-child")
                    node.refresh_from_db()
            else:
                raise ValueError(f"Unknown object type {obj['type']}")

        # nth pass
        # Up to 30 levels deep.
        for i in range(30):
            if Asset.objects.filter(node__isnull=True).count() == 0:
                print("Exit!")
                break

            print(i)

            for obj in data.values():
                if obj["type"] == "asset":
                    asset = Asset.objects.get(assetcode__code=obj["data"]["asset_code"])
                    if Node.objects.filter(asset=asset).count() == 1:
                        continue

                    if obj["data"]["location"].startswith("sr"):
                        parent = AssetCode.objects.get(code=obj["data"]["location"]).asset
                        if parent is not None:
                            try:
                                assert parent.node
                                parent.node.add_child(node_type="A", asset=asset)
                                parent.node.refresh_from_db()
                            except Asset.node.RelatedObjectDoesNotExist:
                                pass
                        else:
                            print(f"WARNING: {obj['data']['location']} is not a valid asset code")
                    else:
                        parent = Node.objects.get(name=obj["data"]["location"], node_type="L")
                        parent.add_child(node_type="A", asset=asset)
                        parent.refresh_from_db()

    def _add_asset(self, data) -> None:
        asset_model, _ = AssetModel.objects.get_or_create(
            name=data["asset_type"],
            manufacturer=self._default_manufacturer,
        )

        asset = Asset.objects.create(
            asset_model=asset_model,
            state="L",
            extra_data=data["data"],
        )

        try:
            AssetCode.objects.get_or_create(asset=asset, code=data["asset_code"], code_type="A")
        except IntegrityError:
            print("WARNING: You have run the import multiple times!")
