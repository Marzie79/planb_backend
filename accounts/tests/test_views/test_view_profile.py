from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import User


class ProfileViewTest(APITestCase):
    def setUp(self):
        self.user = baker.make(User, resume="resume.pdf")
        self.client = APIClient()
        self.data = str(self.user.resume)
        self.client.force_authenticate(user=self.user)
        self.url = '/user/profile/resume/'

    def test_destroy_resume_authenticated(self):
        response = self.client.delete(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_resume_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_resume_not_exist(self):
        user = baker.make(User, resume=None)
        data = str(user.resume)
        response = self.client.delete(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_resume_by_another_user(self):
        random_user = User.objects.create_user(username="Nastaran", password="1234", email="nastaran@gmail.com")
        self.client.force_authenticate(user=random_user)
        response = self.client.delete(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
