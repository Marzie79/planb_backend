from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import User
from core.tests.openapi_tester import BaseAPITestCase


class ProfileViewTest(BaseAPITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_destroy_resume(self):
        self.url = reverse('profile_resume')
        self.user = baker.make(User, resume='resume.pdf')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_picture(self):
        self.url = reverse('profile_picture')
        self.user = baker.make(User, avatar='picture.png')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_profile_endpoints(self):
        self.assertResponse(self.client.get(reverse('profile_brief')))
        self.assertResponse(self.client.get(reverse('profile')))
        self.assertResponse(self.client.get(reverse('profile_picture')))
        self.assertResponse(self.client.get('profile_resume'))
        self.assertResponse(self.client.get(reverse('profile_skills')))
