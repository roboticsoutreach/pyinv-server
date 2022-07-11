from datetime import datetime
from typing import Any

from django.core.management.base import BaseCommand
from django.utils import timezone

from assets.models import Asset


class Command(BaseCommand):

    help = 'Update asset timestamps based on history'  # noqa: A003

    def handle(self, *args: Any, **options: Any) -> None:

        unknown_date = datetime.fromtimestamp(0, timezone.get_current_timezone())

        for asset in Asset.objects.all():

            # Disable auto_now temporarily
            for field in asset._meta.fields:
                if field.name == 'updated_at':
                    field.auto_now = False  # type: ignore

            if asset.assetevent_set.count() == 0:
                # Not all assets have history, some history was destroyed in a rebase in 2014.
                asset.created_at = unknown_date
                asset.updated_at = unknown_date
            else:
                asset.created_at = asset.assetevent_set.order_by(  # type: ignore
                    "changeset__timestamp",
                ).first().changeset.timestamp
                asset.updated_at = asset.assetevent_set.order_by(  # type: ignore
                    "changeset__timestamp"
                ).last().changeset.timestamp

            asset.save(update_fields=["created_at", "updated_at"])
