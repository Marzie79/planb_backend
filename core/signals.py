import os
import uuid

from django.db.models import Model

from accounts.models import *
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

for subclass in AbstractImageModel.__subclasses__():
    @receiver(models.signals.post_delete, sender=subclass)
    def auto_delete_file_on_delete(sender, instance, **kwargs):
        image = getattr(instance, instance.getImageField())
        if image:
            if os.path.isfile(image.path) and str(image.path).find('default') == -1:
                os.remove(image.path)

for subclass in AbstractImageModel.__subclasses__():
    @receiver(models.signals.pre_save, sender=subclass)
    def auto_delete_file_on_change(sender, instance, **kwargs):
        if not instance.pk:
            return False
        try:
            db_model = sender.objects.get(pk=instance.pk)
            old_file = getattr(db_model, db_model.getImageField())
        except Model.DoesNotExist:
            return False
        new_file = getattr(instance, instance.getImageField())
        if old_file.url and not old_file.url == new_file.url and str(old_file.path).find('default') == -1:
            try:
                os.remove(old_file.path)
            except:
                pass
