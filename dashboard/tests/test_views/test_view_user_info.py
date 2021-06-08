from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import User
from core.tests.openapi_tester import BaseAPITestCase


class UserInfoViewTest(BaseAPITestCase):
    def setUp(self):
        self.client = APIClient()
        user = baker.make(User)
        self.list_url = reverse('user-list')
        self.detail_url = reverse('user-detail', kwargs={'username': user.username})

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_info_endpoints(self):
        self.assertResponse(self.client.get(self.list_url))
        self.assertResponse(self.client.get(self.detail_url))


class UserInfoProjectsViewTest(BaseAPITestCase):
    def setUp(self):
        self.client = APIClient()
        user = baker.make(User)
        self.list_url = reverse('user_info_projects-list', kwargs={'slug_username': user.username})

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_info_endpoints(self):
        self.assertResponse(self.client.get(self.list_url))
