from django.test import TestCase
from accounts.models import User
from model_mommy import mommy


# this is just example !
# we don't test simple methods
class TestUser(TestCase):
    def setUp(self):
        self.model = mommy.make(User)

    def test_str(self):
        self.assertEqual(self.model.__str__(), self.model.first_name + ' ' + self.model.last_name)
