from django.contrib.auth.models import User
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

    def validate_first_name(self, value: str) -> str:
        if len(value) < 1:
            raise serializers.ValidationError("Expected at least 1 character")
        return value

    def validate_last_name(self, value: str) -> str:
        if len(value) < 1:
            raise serializers.ValidationError("Expected at least 1 character")
        return value
