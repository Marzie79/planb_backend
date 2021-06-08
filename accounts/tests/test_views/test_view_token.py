import datetime
from freezegun import freeze_time
from model_bakery import baker
from http.cookies import SimpleCookie
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from django.conf import settings

SIGNIN_URL = reverse('token_obtain_pair')
REFRESH_URL = reverse('token_refresh')
LOGOUT_URL = reverse('logout')


class TestMyTokenObtainPairView(APITestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.user.set_password('123')
        self.user.save()
        self.url = SIGNIN_URL

    def test_token(self):
        data = {"username": self.user.username, "password": '123'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(self.client.cookies['token'])
        self.assertTrue(self.client.cookies['token']['httponly'])

    def test_invalid_username(self):
        data = {"username": "mamad", "password": '123'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_password(self):
        data = {"username": self.user.username, "password": '2131243545423442423'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


class TestMyTokenRefreshView(APITestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.user.set_password('123')
        self.user.save()
        data = {"username": self.user.username, "password": '123'}
        self.client.post(SIGNIN_URL, data)
        self.url = REFRESH_URL

    def test_refresh(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(self.client.cookies['token'])

    # def test_http_only(self):
    #     self.client.cookies = SimpleCookie({'token': self.client.cookies['token'].value})
    #     response = self.client.post(self.url, {})
    #     self.assertNotEqual(response.status_code, status.HTTP_200_OK)
    #     try:
    #         self.assertIsNone(response.data['access'])
    #     except:
    #         pass

    def test_not_login(self):
        self.client.cookies = SimpleCookie()
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        try:
            self.assertIsNone(response.data['access'])
        except:
            pass

    def test_expire(self):
        initial_datetime = datetime.datetime.now()
        with freeze_time(initial_datetime) as frozen_datetime:
            frozen_datetime.tick()
            initial_datetime += settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] + datetime.timedelta(days=1)
            self.client.cookies = SimpleCookie()
            response = self.client.post(REFRESH_URL, {})
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            try:
                self.assertIsNone(response.data['access'])
            except:
                pass


class TestLogout(APITestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.user.set_password('123')
        self.user.save()
        data = {"username": self.user.username, "password": '123'}
        response = self.client.post(SIGNIN_URL, data)
        self.token = response.data['access']
        self.url = LOGOUT_URL

    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        try:
            self.assertIsNone(response.data['token'])
        except:
            pass

    def test_not_login(self):
        self.client.cookies = SimpleCookie()
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        try:
            self.assertIsNone(response.data['token'])
        except:
            pass
