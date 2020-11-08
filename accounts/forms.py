from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from .models import *
from django.utils.translation import gettext_lazy


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"), required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm Password'), required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("an error has occurred")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
