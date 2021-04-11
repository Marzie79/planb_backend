
from django.db import models
from django.utils.translation import gettext_lazy as _

class Reciever(models.Model):
    message = models.ForeignKey("Message", verbose_name=_("Message"), on_delete=models.CASCADE)
    user = models.ForeignKey("User", verbose_name=_("User"), on_delete=models.CASCADE)
    is_visited = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Reciever")
        verbose_name_plural = _("Recievers")
        unique_together = ['message', 'user']

    def __str__(self):
        return "%s - %s"%(self.user, self.message)
