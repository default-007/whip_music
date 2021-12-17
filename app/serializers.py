from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedRelatedField(
        view_name="profile-detail", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "url",
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "profile",
        )


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "url",
            "id",
            "user",
            "payment_status",
            "is_premium",
            "location",
            "contact",
        )
