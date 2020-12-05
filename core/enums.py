from enum import Enum
from django.utils.translation import gettext_lazy as _


class FileSize(Enum):
    B = _('Byte')
    KB = _('Kilobyte')
    MB = _('Megabyte')
