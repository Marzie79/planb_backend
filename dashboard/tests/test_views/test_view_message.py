from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from core.tests.openapi_tester import BaseAPITestCase


class MessageViewTest(BaseAPITestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.url_list = reverse('message-list')

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_with_page(self):
        response = self.client.get(self.url_list, {'page': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_endpoints(self):
        self.assertResponse(self.client.get(self.url_list))
