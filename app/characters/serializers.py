from rest_framework import serializers
from .models import Character

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = [
            "id",
            "name",
            "status",
            "species",
            "type",
            "gender",
            "origin_name",
            "origin_url",
            "location_name",
            "location_url",
            "image",
            "url",
            "created",
        ]

