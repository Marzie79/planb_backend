from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from accounts.forms import UserForm


class TestUserForm(TestCase):
    def setUp(self):
        self.form_data = { 'username': 'bardi', 'email': 'bardi@bardi.com',
                     'first_name': _(
                         'First_Name'), 'last_name': _('Last_Name')}

    def test_form_correct(self):
        form_data = {** self.form_data , 'password1': '123', 'password2': '123',}
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertIsNotNone(form.save())

    def test_form_not_password(self):
        form_data = {** self.form_data }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_incorrect_passwordt(self):
        form_data = {** self.form_data , 'password1': '123', 'password2': '1243',}
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())

