from rest_framework import serializers

from assets.models import Manufacturer


class ManufacturerLinkSerializer(serializers.ModelSerializer):
    """Serializer with enough information to display a link to a manufacturer."""

    slug = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = Manufacturer
        fields = ('name', 'slug')


class ManufacturerSerializer(ManufacturerLinkSerializer):
    """Serializer with all information we have about a manufacturer."""

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Manufacturer
        fields = ManufacturerLinkSerializer.Meta.fields + ('created_at', 'updated_at')
