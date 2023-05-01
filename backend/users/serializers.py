from rest_framework import serializers

from .models import CustomUser


class CustomUserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed Serializer for CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_image",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
        ]


class CustomUserMinimalSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model - minimal public data.
    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "profile_image",
        ]
