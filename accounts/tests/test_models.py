from django.test import TestCase
from accounts.models import User, AbstractImageModel
from model_mommy import mommy
from django.core.files.uploadedfile import SimpleUploadedFile
import inspect


class TestAbstractImageModel(TestCase):
    # it's so bad !
    def test_all(self):
        for subclass in AbstractImageModel.__subclasses__():
            self.assertIsNotNone(subclass.getUploadTo())
            try:
                imageName = subclass.getImageName()
            except:
                self.fail()
            if imageName:
                self.assertIsNotNone(getattr(subclass, imageName))
            self.assertIsNotNone(getattr(subclass, subclass.getImageField()))


# this is just example !
# we don't test simple methods
class TestUser(TestCase):
    def setUp(self):
        self.model = mommy.make(User)

    def test_str(self):
        self.assertEqual(self.model.__str__(), self.model.first_name + ' ' + self.model.last_name)
