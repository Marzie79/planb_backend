from django.urls import reverse
from locust import HttpUser, task

import django
import os
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planB_backend.settings.local")
django.setup()

from accounts.models import Temp, User

SIGNIN_URL = reverse('token_obtain_pair')
VERIFY_URL = reverse('verify')
PROJECT_DETAIL_URL = reverse('project-detail', kwargs={'slug': 'تیکتینگ'})
PROJECT_MEMBER_URL = reverse('project_members-list', kwargs={'slug_slug': 'تیکتینگ'})
USER_DETAIL_URL = reverse('user-detail', kwargs={'username': 'superuser'})
USER_PROJECT_URL = reverse('user_info_projects-list', kwargs={'slug_username': 'superuser'})
PROJECTS_LIST_URL = reverse('project-list')
USERS_LIST_URL = reverse('user-list')


class UserData:
    @staticmethod
    def prepare_login_data():
        username = "superuser"
        password = "123"
        data = {"username": username, "password": password}
        return data

    @staticmethod
    def prepare_varify_data():
        Temp.objects.create(email="example@gmail.com", code='1234')
        post_data = {'user': {'email': 'example@gmail.com',
                              'username': 'example',
                              'password': '1234',
                              'first_name': 'نمونه',
                              'last_name': 'نمونه', },
                     "temp": {"code": "1234"}
                     }
        return post_data

    @staticmethod
    def clear_varify_data():
        clear_temps = Temp.objects.filter(email="example@gmail.com")
        clear_users = User.objects.filter(username='example')
        for clear_user in clear_users:
            clear_user.delete()
        for clear_temp in clear_temps:
            clear_temp.delete()


class UserSet(HttpUser):
    @task
    def login(self):
        self.client.post(SIGNIN_URL, data=UserData.prepare_login_data())

    # @task
    # def varify_password(self):
    #     self.client.post(VERIFY_URL, data= json.dumps(UserData.prepare_varify_data()), headers={"content_type": "application/json"},)
    #     UserData.clear_varify_data()


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


class ListSet(HttpUser):
    @task
    def projects_list(self):
        self.client.get(PROJECTS_LIST_URL)

    @task
    def users_list(self):
        self.client.get(USERS_LIST_URL)
