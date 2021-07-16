from django.urls import reverse
from locust import HttpUser, task

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planB_backend.settings.local")
django.setup()

# from accounts.models.user import User
# from model_bakery import baker
# import json

SIGNIN_URL = reverse('token_obtain_pair')
VERIFY_URL = reverse('verify')
SIGNUP_URL = reverse('signup')

def prepare_login_data():
    username = "nimapr"
    password = "123"
    data = {"username": username, "password": password}
    return data


class UserSet(HttpUser):
    @task
    def login(self):
        self.client.post(SIGNIN_URL, data=prepare_login_data())

    # @task
    # def signup(self):
    #     self.client.post(SIGNUP_URL, data={"email": "paryfardnim@gmail.com"})

    # @task
    # def varify(self):
    #     self.client.post(VERIFY_URL, data=)

