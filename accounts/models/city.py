from django.db import models
from django.utils.translation import gettext_lazy as _

class City(models.Model):
    province = models.ForeignKey("Province", verbose_name=_("Province"), on_delete=models.PROTECT)
    name = models.CharField(_("City_name"), max_length=20, unique=True)
    code = models.CharField(_("City_Code"), max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Cities")
        verbose_name = _("City")
        unique_together = ('name', 'province',)
