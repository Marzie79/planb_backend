from django.contrib.auth.models import BaseUserManager
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import raise_errors_on_nested_writes


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        # set an algorithm to not show password directly
        user.set_password(password)
        user.save(using=self._db)
        return user

    # fields that we want get it from user when we want to create superuser
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


