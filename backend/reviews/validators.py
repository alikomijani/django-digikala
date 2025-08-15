from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_rate(value):
    if value > 5:
        raise ValidationError(
            _("%(value)s must less then or equal 5"),
            params={"value": value},
        )
    if value < 0:
        raise ValidationError(
            _("%(value)s must more then or equal 0"),
            params={"value": value},
        )
