from django.contrib.auth.models import User
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)

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


class UserLinkSerializer(serializers.ModelSerializer):

    username = serializers.CharField(read_only=True)
    display_name = serializers.SerializerMethodField("get_display_name", read_only=True)

    def get_display_name(self, user: User) -> str:
        return user.get_full_name() or user.username

    class Meta:
        model = User
        fields = (
            'username',
            'display_name',
        )
