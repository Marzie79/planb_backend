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
PROJECT_DETAIL_URL = reverse('project-detail', kwargs={'slug': 'تیکتینگ'})
PROJECT_MEMBER_URL = reverse('project_members-list', kwargs={'slug_slug': 'تیکتینگ'})
USER_DETAIL_URL = reverse('user-detail', kwargs={'username': 'superuser'})
USER_PROJECT_URL = reverse('user_info_projects-list', kwargs={'slug_username': 'superuser'})


def prepare_login_data():
    username = "superuser"
    password = "123"
    data = {"username": username, "password": password}
    return data


class UserSet(HttpUser):
    @task
    def login(self):
        self.client.post(SIGNIN_URL, data=prepare_login_data())


class ProjectDetailSet(HttpUser):
    @task
    def project_detail(self):
        self.client.get(PROJECT_DETAIL_URL)

    @task
    def project_member_detail(self):
        self.client.get(PROJECT_MEMBER_URL)


class UserDeailSet(HttpUser):
    @task
    def user_detail(self):
        self.client.get(USER_DETAIL_URL)

    @task
    def user_project_detail(self):
        self.client.get(USER_PROJECT_URL)

# @task
# def signup(self):
#     self.client.post(SIGNUP_URL, data={"email": "paryfardnim@gmail.com"})

# @task
# def varify(self):
#     self.client.post(VERIFY_URL, data=)
