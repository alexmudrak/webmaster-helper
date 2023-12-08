from api.abstract.serializers import AbstractSerializer
from api.webmaster.models import Payment
from api.webmaster.serializers.webmaster import WebmasterLessSerializer


class PaymentSerializer(AbstractSerializer):
    webmaster = WebmasterLessSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "type",
            "details",
            "webmaster",
        ]
