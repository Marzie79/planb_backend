from django.db import models
from django.utils.translation import gettext_lazy as _



class University(models.Model):
    city = models.ForeignKey("City", verbose_name=_("City"), on_delete=models.PROTECT)
    name = models.CharField(_("University_name"), max_length=20)
    code = models.CharField(_("University_code"), max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Universities")
        verbose_name = _("University")
        unique_together = ('name', 'city',)