import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase , APIClient, RequestsClient
from model_bakery import baker
from accounts.models import *
from core.tests.openapi_tester import BaseAPITestCase


class UserProjectViewTest(BaseAPITestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.user_project_pending = baker.make(UserProject,status="PENDING", user=self.user)
        self.user_project_declined = baker.make(UserProject,status="DECLINED", user=self.user)
        self.user_project_accepted = baker.make(UserProject,status="ACCEPTED", user=self.user)
        self.user_project_admin = baker.make(UserProject,status="ADMIN", user=self.user)
        self.user_project_creator = baker.make(UserProject,status="CREATOR", user=self.user)
        self.client = APIClient()
        self.client1 = RequestsClient()
        self.url = reverse('user_projects')
    
    def test_category_project(self):
        data = {"category":"PROJECT"}
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, data)
        user_projects = json.loads(response.content)
        for item in user_projects:
            if item["role"] not in ["ادمین", "سازنده", "عضو تیم"]:
                assert(status.HTTP_400_BAD_REQUEST_)
        assert response.status_code == status.HTTP_200_OK

    def test_category_request(self):
        data = {"category":"REQUEST"}
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, data)
        user_projects = json.loads(response.content)
        for item in user_projects:
            if item["status"]["code"] not in ["DECLINED", "PENDING"]:
                assert(status.HTTP_400_BAD_REQUEST_)
        assert response.status_code == status.HTTP_200_OK

    def test_category_project_admin(self):
        data = {"category":"PROJECT", "status":"ADMIN"}
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, data)
        user_projects = json.loads(response.content)
        for item in user_projects:
            if item["role"] not in ["ادمین"]:
                assert(status.HTTP_400_BAD_REQUEST_)
        assert response.status_code == status.HTTP_200_OK


    def test_category_project_creator(self):
        data = {"category":"PROJECT", "status":"CREATOR"}
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, data)
        user_projects = json.loads(response.content)
        for item in user_projects:
            if item["role"] not in ["سازنده"]:
                assert(status.HTTP_400_BAD_REQUEST_)
        assert response.status_code == status.HTTP_200_OK


    def test_category_project_accepted(self):
        data = {"category":"PROJECT", "status":"ACCEPTED"}
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, data)
        user_projects = json.loads(response.content)
        for item in user_projects:
            if item["role"] not in ["عضو تیم"]:
                assert(status.HTTP_400_BAD_REQUEST_)
        assert response.status_code == status.HTTP_200_OK


    def test_category_request_declined(self):
        data = {"category":"REQUEST", "status":"DECLINED"}
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, data)
        user_projects = json.loads(response.content)
        for item in user_projects:
            if item["status"]["code"] not in ["DECLINED"]:
                assert(status.HTTP_400_BAD_REQUEST_)
        assert response.status_code == status.HTTP_200_OK


    def test_category_request_pending(self):
        data = {"category":"REQUEST", "status":"PENDING"}
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, data)
        user_projects = json.loads(response.content)
        for item in user_projects:
            if item["status"]["code"] not in ["PENDING"]:
                assert(status.HTTP_400_BAD_REQUEST_)
        assert response.status_code == status.HTTP_200_OK


    def test_authenticate_of_this_api(self):
        data = {"category":"REQUEST"}
        response = self.client1.get("http://api"+self.url, json=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_rwquest_without_date(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        user_projects = json.loads(response.content)
        for item in user_projects:
            if item["role"] not in ["ادمین", "سازنده", "عضو تیم"]:
                assert(status.HTTP_400_BAD_REQUEST_)
        assert response.status_code == status.HTTP_200_OK


    def test_user_project_endpoints(self):
        self.assertResponse(self.client.get(self.url))

