from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import User


class ProfileViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/user/profile/resume/'

    def test_destroy_resume_not_exist(self):
        user = baker.make(User, resume=None)
        self.client.force_authenticate(user=user)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

