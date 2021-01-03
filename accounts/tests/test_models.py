from django.test import TestCase
from accounts.models import User, AbstractImageModel
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile
import inspect

# this is just example !
# we don't test simple methods
class TestUser(TestCase):
    def setUp(self):
        self.model = baker.make(User)

    def test_str(self):
        self.assertEqual(self.model.__str__(), self.model.first_name + ' ' + self.model.last_name)
