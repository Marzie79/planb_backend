from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationToken(models.Model):
    user = models.ForeignKey("User", verbose_name=_("User"), blank=True, null=True, on_delete=models.CASCADE)
    browser = models.CharField(_("Browser"), max_length=100, blank=True, null=True)
    device = models.CharField(_("Device"), max_length=100, blank=True, null=True)
    token = models.TextField(_("Token"), blank=True, null=True)

    class Meta:
        verbose_name = _("Notification")
        unique_together = ('user', 'browser', 'device')