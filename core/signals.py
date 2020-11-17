import os
import uuid
from accounts.models import *
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


for subclass in AbstractImageModel.__subclasses__():
    @receiver(models.signals.post_delete, sender=subclass)
    def auto_delete_file_on_delete(sender, instance, **kwargs):
        image = getattr(instance,instance.getImageField())
        if image:
            if os.path.isfile(image.path) and str(image.path).find('default') == -1:
                os.remove(image.path)

for subclass in AbstractImageModel.__subclasses__():
    @receiver(models.signals.pre_save, sender=subclass)
    def auto_delete_file_on_change(sender, instance, **kwargs):
        if not instance.pk:
            return False
        try:
            model = sender.objects.get(pk=instance.pk)
            old_file = getattr(model,model.getImageField())
        except User.DoesNotExist:
            return False
        new_file = getattr(instance,model.getImageField())
        if not old_file == new_file:
            # if os.path.isfile(old_file.path):
            if instance.avatar_thumbnail.url and str(old_file.path).find('default') == -1:
                try:
                    os.remove(old_file.path)
                except:
                    pass
