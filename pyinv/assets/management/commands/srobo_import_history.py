import json
from datetime import datetime
from pathlib import Path
from typing import Any

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandParser
from django.db.models import Count
from django.utils import timezone

from assets.models import Asset, AssetEvent, ChangeSet

CHANGE_TYPE_MAP = {
    'move': AssetEvent.AssetEventType.MOVE,
    'added': AssetEvent.AssetEventType.CREATE,
}


class Command(BaseCommand):

    help = 'Import asset history from Student Robotics JSON format'  # noqa: A003

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('data_dir', type=Path)

    def handle(self, *args: Any, **options: Any) -> None:
        data_dir: Path = options['data_dir']
        self.stdout.write(f"Importing history from {data_dir}")

        # Delete all of the events before starting.
        ChangeSet.objects.all().delete()
        assert AssetEvent.objects.count() == 0

        for file in sorted(data_dir.iterdir()):  # Sort by timestamp in filename
            data = json.loads(file.read_text())
            user, _ = User.objects.update_or_create(
                username=data['author_email'],
                email=data['author_email'],
                is_active=False,
            )

            cs, _ = ChangeSet.objects.get_or_create(
                user=user,
                comment=data["message"],
                timestamp=datetime.fromtimestamp(data["dt"], timezone.get_current_timezone())
            )

            for change in data["changes"]:
                code = change.pop("asset_code").strip()
                change_type = change.pop("type")
                data = change

                try:
                    asset = Asset.objects.filter(assetcode__code=code).get()
                except Asset.DoesNotExist:
                    continue

                # If the asset has been deleted and un-deleted, mark it as restored from lost.
                if change_type == "added" and asset.assetevent_set.filter(event_type="CR").exists():
                    change_type = "move"
                    data = {
                        "old": None,
                        "new": change["location"]
                    }

                event_type = CHANGE_TYPE_MAP[change_type]
                cs.assetevent_set.create(asset=asset, event_type=event_type, data=data)

            # Delete empty changesets.
            ChangeSet.objects.annotate(event_count=Count("assetevent__id")).filter(event_count=0).delete()
