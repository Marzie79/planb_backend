from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from .enums import FileSize
from .utils import FileUtils
##db validators
from rest_framework import serializers

ENGLISH_REGEX_VALIDATOR_MESSAGE = _("Must only contain English letters and numbers.")
ENGLISH_REGEX_VALIDATOR = RegexValidator(regex='^[a-zA-Z0-9]+$', message=ENGLISH_REGEX_VALIDATOR_MESSAGE)

CHAR_REGEX_VALIDATOR_MESSAGE = _("It should only contain English letters and numbers and special letters.")
CHAR_REGEX_VALIDATOR = RegexValidator(regex=r'^[\w.@+-]+$', message=CHAR_REGEX_VALIDATOR_MESSAGE)

PERSIAN_REGEX_VALIDATOR_MESSAGE = _("It should only contain Persian letters.")
PERSIAN_REGEX_VALIDATOR = RegexValidator(regex='^[\u0600-\u06FF\s]+$', message=PERSIAN_REGEX_VALIDATOR_MESSAGE)

##translated message
PHONE_NUMBER_REGEX_VALIDATOR_MESSAGE = _("The phone number entered is not valid.")
JWT_NOT_FOUND_MESSAGE = _("No active account found with the given credentials")


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


# file type validators

def validate_pdf_type(value):
    return validate_file_type(value, ['.pdf'])


# file type validators
def validate_file_type(value, types):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    if not ext.lower() in types:
        raise ValidationError(_("File type must be {}").format(','.join(types)))
