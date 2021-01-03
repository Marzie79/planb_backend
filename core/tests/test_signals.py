import random
from django.test import TestCase
from accounts.models import User, AbstractImageModel
import tempfile
from model_bakery import baker

# class TestChangePictureSignal(TestCase):
#
#     def setUp(self):
#         model_class = random.choice(AbstractImageModel.__subclasses__())
#         tempfile.NamedTemporaryFile(suffix=".jpg").name
#         self.image_field = model_class.getImageField()
#         self.model = baker.make(model_class,_create_files=True)
#         self.old_image =getattr(self.model,self.image_field)
#
#     def test_change_picture(self):
#         new_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
#         setattr(self.model, self.image_field, new_image)
#         self.model.save()
#         self.assertNotEqual(self.old_image,getattr(self.model,self.image_field))

