import jdatetime
from django.db import models
from django.utils.translation import gettext_lazy as _


class Message(models.Model):
    text = models.TextField(_("Text"))
    created_date = models.DateTimeField(_("Created Date"), auto_now_add=True)
    project = models.ForeignKey("Project", on_delete=models.SET_NULL, null = True , blank=True)


    class Meta:
        ordering = ['-id']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return self.text

    def created_date_decorated(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_date).strftime("%a, %d %b %Y %H:%M:%S")

    created_date_decorated.short_description = _("Created_Date_Decorated")
