from rest_framework import serializers

from .models import CustomUser


class CustomUserURLRepresentationMixin(serializers.ModelSerializer):
    """
    Deliver consistent relative URLs of user profile images.
    """

    def to_representation(self, instance):
        """
        Deliver consistent relative URLs of user profile images.
        Issue: https://forum.djangoproject.com/t/drf-imagefield-serializes-entire-url-with-domain-name/6975
        """
        ret = super().to_representation(instance)
        ret["profile_image"] = (
            instance.profile_image.url if instance.profile_image else ""
        )
        ret["profile_image_thumbnail_small"] = (
            instance.profile_image_thumbnail_small.url if instance.profile_image else ""
        )
        ret["profile_image_thumbnail_large"] = (
            instance.profile_image_thumbnail_large.url if instance.profile_image else ""
        )
        return ret


class CustomUserDetailSerializer(
    CustomUserURLRepresentationMixin, serializers.ModelSerializer
):
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
            "profile_image_thumbnail_small",
            "profile_image_thumbnail_large",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
        ]


class CustomUserMinimalSerializer(
    CustomUserURLRepresentationMixin, serializers.ModelSerializer
):
    """
    Serializer for CustomUser model - minimal public data.
    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "profile_image",
            "profile_image_thumbnail_small",
            "profile_image_thumbnail_large",
        ]
