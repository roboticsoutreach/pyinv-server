from accounts.serializers import UserLinkSerializer
from rest_framework import serializers

from assets.models import ChangeSet


class ChangeSetSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)  # noqa: A003
    timestamp = serializers.DateTimeField(read_only=True)
    user = UserLinkSerializer(read_only=True)
    comment = serializers.CharField(read_only=True)

    class Meta:
        model = ChangeSet
        fields = ('id', 'timestamp', 'display_name', 'user', 'comment')


class ChangeSetSerializerWithCountSerializer(ChangeSetSerializer):

    event_count = serializers.IntegerField(read_only=True, source="assetevent_set.count")

    class Meta:
        model = ChangeSet
        fields = ('id', 'timestamp', 'display_name', 'user', 'comment', 'event_count')
