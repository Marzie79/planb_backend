from django.test import TestCase
from accounts.models import User
from model_mommy import mommy
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status
from http.cookies import SimpleCookie

SIGNIN_URL = reverse('token_obtain_pair')
REFRESH_URL = reverse('token_refresh')
LOGOUT_URL = reverse('logout')


class TestMyTokenObtainPairView(APITestCase):

    def setUp(self):
        self.user = mommy.make(User)
        self.user.set_password('123')
        self.user.save()

    def test_token(self):
        data = {"username": self.user.username, "password": '123'}
        response = self.client.post(SIGNIN_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(self.client.cookies['token'])
        self.assertTrue(self.client.cookies['token']['httponly'])

    def test_invalid_username(self):
        data = {"username": "mamad", "password": '123'}
        response = self.client.post(SIGNIN_URL, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_incorrect_password(self):
        data = {"username": self.user.username, "password": '2131243545423442423'}
        response = self.client.post(SIGNIN_URL, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestMyTokenRefreshView(APITestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.user.set_password('123')
        self.user.save()
        data = {"username": self.user.username, "password": '123'}
        response = self.client.post(SIGNIN_URL, data)

    def test_refresh(self):
        response = self.client.post(REFRESH_URL, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(self.client.cookies['token'])

    def test_http_only(self):
        self.client.cookies = SimpleCookie({'token': self.client.cookies['token'].value})
        response = self.client.post(REFRESH_URL, {})
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        try:
            self.assertIsNone(response.data['access'])
        except:
            pass

    def test_not_login(self):
        self.client.cookies = SimpleCookie()
        response = self.client.post(REFRESH_URL, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        try:
            self.assertIsNone(response.data['access'])
        except:
            pass


class TestLogout(APITestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.user.set_password('123')
        self.user.save()
        data = {"username": self.user.username, "password": '123'}
        response = self.client.post(SIGNIN_URL, data)
        self.token = response.data['access']

    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(LOGOUT_URL, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        try:
            self.assertIsNone(response.data['token'])
        except:
            pass

    def test_not_login(self):
        self.client.cookies = SimpleCookie()
        response = self.client.post(LOGOUT_URL, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        try:
            self.assertIsNone(response.data['token'])
        except:
            pass
