from rest_framework import serializers

from .models import ArizonaBirds

class GBIFSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArizonaBirds
        fields = (
            "id",
            "gbifid",
            "individualcount",
            "date",
            "genus",
            "species"
        )
