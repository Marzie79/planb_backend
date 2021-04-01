from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .enums import FileSize
from .utils import FileUtils
from rest_framework import serializers


##db validators

@deconstructible
class FileTypeValidator:
    message = _("File type must be {}")

    def __init__(self, type):
        self.type = type
        if not self.type or not isinstance(self.type, str):
            raise TypeError("types must be String")

    def __call__(self, value):
        import os
        from django.core.exceptions import ValidationError
        ext = os.path.splitext(value.name)[1][1:]  # [0] returns path+filename
        if not ext.lower() == self.type:
            raise ValidationError(self.message.format(self.type))

    def __eq__(self, other):
        return (
                isinstance(other, FileTypeValidator) and
                self.type == other.type
        )


ENGLISH_REGEX_VALIDATOR_MESSAGE = _("Must only contain English letters and numbers.")
ENGLISH_REGEX_VALIDATOR = RegexValidator(regex='^[a-zA-Z0-9]+$', message=ENGLISH_REGEX_VALIDATOR_MESSAGE)

CHAR_REGEX_VALIDATOR_MESSAGE = _("It should only contain English letters and numbers and special letters.")
CHAR_REGEX_VALIDATOR = RegexValidator(regex=r'^[\w.@+-]+$', message=CHAR_REGEX_VALIDATOR_MESSAGE)

PERSIAN_REGEX_VALIDATOR_MESSAGE = _("It should only contain Persian letters.")
PERSIAN_REGEX_VALIDATOR = RegexValidator(regex='^[\u0600-\u06FF\s]+$', message=PERSIAN_REGEX_VALIDATOR_MESSAGE)

PDF_TYPE_VALIDATOR = FileTypeValidator('pdf')
SVG_TYPE_VALIDATOR = FileTypeValidator('svg')

##translated message
PHONE_NUMBER_REGEX_VALIDATOR_MESSAGE = _("The phone number entered is not valid.")
JWT_NOT_FOUND_MESSAGE = _("No active account found with the given credentials")
PERMISSION_DENY = _("You do not have permission to perform this action.")

##serializer validators

class FileSizeValidator:
    def __init__(self, size):
        ## get size in megabyte
        self.size = size

    def __call__(self, file):
        for key, value in file.items():
            if value.size > FileUtils.convert_to_byte(self.size, FileSize['MB'].name):
                message = _('The photo size should be more than {} {}').format(self.size, FileSize['MB'].value)
                raise serializers.ValidationError({key: [message]})


# enums
MAX_IMAGE_SIZE = 5  # 12000000
MAX_FILE_SIZE = 5
