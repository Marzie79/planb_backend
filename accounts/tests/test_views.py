import datetime
import json
from freezegun import freeze_time
from model_mommy import mommy
from http.cookies import SimpleCookie
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils import timezone
from accounts.models import User, Temp
from django.utils.translation import gettext_lazy as _

SIGNIN_URL = reverse('token_obtain_pair')
REFRESH_URL = reverse('token_refresh')
LOGOUT_URL = reverse('logout')
SIGNUP_URL = reverse('signup')
REQUESTPASSWORD_URL = reverse('reset_password')


class ResetPasswordTest(APITestCase):
    def setUp(self):
        for i in range(1, 10):
            user = mommy.make(User)
            Temp.objects.create(email=user.email, date=timezone.now(),
                                code=get_random_string(length=16))
        self.user = mommy.make(User)
        self.user.email = "paryfardnim@gmail.com"
        self.user.username = "nimapr"
        self.user.set_password('1234')
        self.user.save()
        self.temp = mommy.make(Temp)
        self.temp.email = 'paryfardnim@gmail.com'
        self.temp.code = '1234'
        self.temp.save()
        self.data = {
            "temp": {
                "code": self.temp.code,
                "email": self.temp.email
            },
            "password": "122346"
        }
        self.jsondata = json.dumps(self.data)
        # self.token = TokenObtainPairSerializer(
        #     {'username': self.user.username, 'password': self.user.password}).validate()
        self.refreshtoken = RefreshToken.for_user(self.user)
        self.accesstoken = self.refreshtoken.access_token

    def test_password_changed(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.accesstoken))
        response = client.patch(REQUESTPASSWORD_URL, self.jsondata, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(client.cookies['token'])

    def test_temp_is_not_existed(self):
        self.data['temp']['code'] = "123456789"
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.accesstoken))
        jsondata = json.dumps(self.data)
        response = client.patch(REQUESTPASSWORD_URL, jsondata, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def user_is_not_authenticated(self):
        response = self.client.patch(REQUESTPASSWORD_URL, self.jsondata, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class VerifyAccountTest(APITestCase):
    def setUp(self):
        for i in range(1, 10):
            another_user = mommy.make(User)
            Temp.objects.create(email=another_user.email, date=timezone.now(),
                                code=get_random_string(length=16))
        self.user = mommy.make(User)
        self.user.email = "paryfardnim@gmail.com"
        self.user.username = 'nimapr'
        self.user.set_password('1234')
        self.user.save()
        temp = mommy.make(Temp)
        temp.email = 'paryfardnim@gmail.com'
        temp.code = '1234'
        temp.save()
        self.post_data = {'user.email': 'example@gmail.com',
                          'user.username': 'example',
                          'user.password': '1234',
                          'user.first_name': _('example'),
                          'user.last_name': _('example'),
                          'username': 'example',
                          'password': '1234'}

    def test_temp_is_existed_get(self):
        data = {'code': '1234'}
        user_temp = Temp.objects.get(code=data['code'])
        response = self.client.get(reverse('verify'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(user_temp)

    def test_temp_is_not_existed_get(self):
        data = {'code': '4321'}
        response = self.client.get(reverse('verify'), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_is_created_post(self):
        user_temp = Temp.objects.create(code='12345', email="example@gmail.com")
        self.post_data['temp.code'] = user_temp.code
        response = self.client.post(reverse('verify'), self.post_data)
        user = User.objects.get(username='example')
        self.assertIsNotNone(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(self.client.cookies['token'])

    def test_temp_is_not_existed_post(self):
        self.post_data['temp.code'] = '41324'
        response = self.client.post(reverse('verify'), self.post_data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestSignUpView(APITestCase):
    def setUp(self):
        for i in range(1, 10):
            user = mommy.make(User)
            Temp.objects.create(email=user.email, date=timezone.now(),
                                code=get_random_string(length=16))

    def test_valid_sent_response_if_temp_is_not_existed(self):
        data = {'email': 'paryfardnim@gmail.com'}
        obj_user = User.objects.filter(email=data['email']).first()
        temp = Temp.objects.filter(email=data['email']).first()
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(obj_user)
        self.assertIsNone(temp)

    def test_valid_sent_response_if_temp_is_existed(self):
        initial_datetime = datetime.datetime.now()
        data = {'email': 'example@gmail.com'}
        obj_user = User.objects.filter(email=data['email']).first()
        temp_example = mommy.make(Temp)
        temp_example.email = 'example@gmail.com'
        temp_example.save()
        with freeze_time(initial_datetime) as frozen_datetime:
            frozen_datetime.tick()
            initial_datetime += datetime.timedelta(minutes=3)
            temp = Temp.objects.filter(email=data['email']).first()
            response = self.client.post(SIGNUP_URL, data)
            self.assertIsNone(obj_user)
            self.assertIsNotNone(temp)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_User_is_existed(self):
        data = {'email': 'paryfardnim@gmail.com'}
        user = mommy.make(User)
        user.email = data['email']
        user.save()
        obj_user = User.objects.filter(email=data['email']).first()
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIsNotNone(response.data['error'])
        self.assertIsNotNone(obj_user)

    def test_time_expired_Temp(self):
        data = {'email': 'paryfardnim@gmail.com'}
        temp = mommy.make(Temp)
        temp.email = data['email']
        temp.data = datetime.datetime.now() - datetime.timedelta(minutes=3)
        temp.save()
        response = self.client.post(SIGNUP_URL, data)
        temp_search = Temp.objects.filter(email=data['email']).first()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'EmailTimeError')
        self.assertIsNotNone(temp_search)
        self.assertEqual(timezone.now() < temp.date + datetime.timedelta(minutes=2), True)


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
