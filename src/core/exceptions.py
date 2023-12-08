from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.views import status


class DuplicateError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("Duplicate error. This entity already exist.")
    default_code = "duplicate_error"
