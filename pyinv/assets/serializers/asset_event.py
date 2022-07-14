from rest_framework import serializers

from assets.models import AssetEvent

from .asset import AssetLinkSerializer
from .changeset import ChangeSetSerializer


class AssetEventWithoutChangeSetSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)  # noqa: A003
    event_type = serializers.ChoiceField(AssetEvent.AssetEventType, read_only=True)
    event_data = serializers.JSONField(source="data", read_only=True)

    class Meta:
        model = AssetEvent
        fields = ('id', 'event_type', 'event_data')


class AssetEventTimelineSerializer(AssetEventWithoutChangeSetSerializer):

    asset = AssetLinkSerializer(read_only=True)

    class Meta:
        model = AssetEvent
        fields = ('id', 'event_type', 'asset', 'event_data')


class AssetEventSerializer(AssetEventWithoutChangeSetSerializer):

    changeset = ChangeSetSerializer(read_only=True)

    class Meta:
        model = AssetEvent
        fields = ('id', 'changeset', 'event_type', 'event_data')


class AssetEventWithAssetSerializer(AssetEventSerializer):

    asset = AssetLinkSerializer(read_only=True)

    class Meta:
        model = AssetEvent
        fields = ('id', 'changeset', 'event_type', 'asset', 'event_data')
