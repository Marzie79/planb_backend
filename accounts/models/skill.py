from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from core.validators import SVG_TYPE_VALIDATOR



class Skill(models.Model):
    name = models.CharField(_("Skill_name"), max_length=30, unique=True)
    code = models.CharField(_("Skill_code"), max_length=10, unique=True)
    skill = models.ForeignKey('self', verbose_name=_("Skill's_Father"), on_delete=models.PROTECT,
                              related_name='child_skill',
                              null=True, blank=True)
    image = models.FileField(_("image"), blank=True, null=True, upload_to='skill/image/',
                             validators=[SVG_TYPE_VALIDATOR])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Skills")
        verbose_name = _("Skill")
