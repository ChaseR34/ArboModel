from rest_framework import serializers

from .models import Pool

class MosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pool
        fields = (
            "id",
            "SampleID",
            "positive",
            "num_female_mos",
            "virus_id",
            "sequenced_id"
        )
