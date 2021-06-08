import jdatetime
from datetime import datetime,timedelta

from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _


class Temp(models.Model):
    email = models.EmailField(_("Email"), validators=[validate_email], max_length=255)
    date = models.DateTimeField(_("Date"), auto_now=True)
    code = models.CharField(_("Code"), max_length=20)

    class Meta:
        ordering = ['date']
        verbose_name = _("Temp")
        verbose_name_plural = _("Temps")

