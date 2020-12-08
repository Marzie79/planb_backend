from django.test import TestCase
from accounts.models import User, AbstractImageModel


class TestAbstractImageModel(TestCase):
    def test_properties(self):
        for subclass in AbstractImageModel.__subclasses__():
            self.assertIsNotNone(subclass.getUploadTo())
            try:
                imageName = subclass.getImageName()
            except:
                self.fail()
            if imageName:
                self.assertIsNotNone(getattr(subclass, imageName))
            self.assertIsNotNone(getattr(subclass, subclass.getImageField()))

