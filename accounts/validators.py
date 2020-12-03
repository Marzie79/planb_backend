from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


ENGLISH_REGEX_VALIDATOR_MESSAGE = _("Must only contain English letters and numbers.")
ENGLISH_REGEX_VALIDATOR = RegexValidator(regex='^[a-zA-Z0-9]+$', message=ENGLISH_REGEX_VALIDATOR_MESSAGE)

CHAR_REGEX_VALIDATOR_MESSAGE = _("It should only contain English letters and numbers and special letters.")
CHAR_REGEX_VALIDATOR = RegexValidator(regex=r'^[\w.@+-]+$', message=CHAR_REGEX_VALIDATOR_MESSAGE)

PERSIAN_REGEX_VALIDATOR_MESSAGE = _("It should only contain Persian letters.")
PERSIAN_REGEX_VALIDATOR = RegexValidator(regex='^[\u0600-\u06FF\s]+$', message=PERSIAN_REGEX_VALIDATOR_MESSAGE)

PHONE_NUMBER_REGEX_VALIDATOR_MESSAGE = _("The phone number entered is not valid.")


#
# def validate_international(value):
#     phone_number = to_python(value)
#     if phone_number and not phone_number.is_valid():
#         raise ValidationError(
#             _("The phone number entered is not valid."), code="invalid_phone_number"
#         )

