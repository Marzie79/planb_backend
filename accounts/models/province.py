from django.db import models
from django.utils.translation import gettext_lazy as _

class Province(models.Model):
    name = models.CharField(_("Province_name"), max_length=20, unique=True)
    code = models.CharField(_("Province_code"), max_length=10, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Provinces")
        verbose_name = _("Province")

    def __str__(self):
        return self.name
