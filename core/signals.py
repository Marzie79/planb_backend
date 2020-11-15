import os
import uuid
from accounts.models import *
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.avatar_thumbnail:
        if os.path.isfile(instance.avatar_thumbnail.path):
            os.remove(instance.avatar_thumbnail.path)

@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = User.objects.get(pk=instance.pk).avatar_thumbnail
    except User.DoesNotExist:
        return False

    new_file = instance.avatar_thumbnail
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)