from imagekit.processors import ResizeToFit
from django.db import models
from core.utils import ImageUtils

# use this for models have image field
# for use this model you must extend this
# and  create   IMAGE_PROCESS , getImageField(cls) getImageName(clsc) , getUploadTo(cls) like userModel
# and delete signal , resize image work for it !
class AbstractImageModel(models.Model):
    IMAGE_PROCESS = {
        "upload_to": ImageUtils(),
        "processors": [ResizeToFit(400, 400)],
        "format": 'JPEG',
        "options": {'quality': 60},
        "default": None
    }

    @classmethod
    def getImageField(cls):
        return None

    @classmethod
    def getImageName(clsc):
        return None

    @classmethod
    def getUploadTo(cls):
        return None

    class Meta:
        abstract = True
