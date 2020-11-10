from django.test import TestCase
from accounts.models import User
from model_mommy import mommy
from rest_framework.test import APIClient,APITestCase
from django.urls import  reverse
from rest_framework import status

class TestMyTokenObtainPairView(APITestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.user.set_password('123')
        self.user.save()

    def test_token(self):
        url = reverse('token_obtain_pair')
        data = {"username" : self.user.username ,"password" : '123'}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(self.client.cookies['token'])

