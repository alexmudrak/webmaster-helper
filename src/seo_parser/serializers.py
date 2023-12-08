from rest_framework import serializers

from seo_parser.models import SeoData


class SeoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoData
        fields = [
            "type",
            "data",
            "created",
        ]
