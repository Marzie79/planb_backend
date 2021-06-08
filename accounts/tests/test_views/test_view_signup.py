import datetime
import json
from freezegun import freeze_time
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils import timezone
from accounts.models import User, Temp
from django.utils.translation import gettext_lazy as _

LOGOUT_URL = reverse('logout')
SIGNUP_URL = reverse('signup')
REQUEST_PASSWORD_URL = reverse('reset_password')
VERIFY = reverse('verify')

class ResetPasswordTest(APITestCase):
    def setUp(self):
        for i in range(1, 10):
            user = baker.make(User)
            Temp.objects.create(email=user.email, date=timezone.now(),
                                code=get_random_string(length=16))
        self.user = baker.make(User, username="nimapr", email="paryfardnim@gmail.com")
        self.user.set_password('1234')
        self.user.save()
        self.temp = baker.make(Temp, email='paryfardnim@gmail.com', code='1234')
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
        self.url = REQUEST_PASSWORD_URL

    def test_password_changed(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.accesstoken))
        response = client.patch(self.url, self.jsondata, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(client.cookies['token'])

    def test_temp_is_not_existed(self):
        self.data['temp']['code'] = "123456789"
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.accesstoken))
        jsondata = json.dumps(self.data)
        response = client.patch(self.url, jsondata, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class VerifyAccountTest(APITestCase):
    def setUp(self):
        self.url = VERIFY
        for i in range(1, 10):
            another_user = baker.make(User)
            Temp.objects.create(email=another_user.email, date=timezone.now(),
                                code=get_random_string(length=16))
        self.user = baker.make(User)
        self.user.email = "paryfardnim@gmail.com"
        self.user.username = 'nimapr'
        self.user.set_password('1234')
        self.user.save()
        temp = baker.make(Temp)
        temp.email = 'paryfardnim@gmail.com'
        temp.code = '1234'
        temp.save()
        self.post_data = {'user': {'email': 'example@gmail.com',
                                   'username': 'example',
                                   'password': '1234',
                                   'first_name': 'نمونه',
                                   'last_name': 'نمونه', }
                          }

    def test_temp_is_existed_get(self):
        data = {'code': '1234'}
        user_temp = Temp.objects.get(code=data['code'])
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(user_temp)

    def test_temp_is_not_existed_get(self):
        data = {'code': '4321'}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_is_created_post(self):
        user_temp = Temp.objects.create(code='12345', email="example@gmail.com")
        self.post_data['temp'] = {"code": user_temp.code, }
        response = self.client.post(self.url, json.dumps(self.post_data), content_type="application/json")
        user = User.objects.get(username='example')
        self.assertIsNotNone(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(self.client.cookies['token'])

    def test_temp_is_not_existed_post(self):
        self.post_data['temp'] = {"code": '41324'}
        response = self.client.post(self.url, self.post_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestSignUpView(APITestCase):
    def setUp(self):
        self.data = {'email': 'paryfardnim@gmail.com'}
        self.url = SIGNUP_URL
        for i in range(1, 10):
            user = baker.make(User)
            Temp.objects.create(email=user.email, date=timezone.now(),
                                code=get_random_string(length=16))

    def test_valid_sent_response_if_temp_is_not_existed(self):
        obj_user = User.objects.filter(email=self.data['email']).first()
        temp = Temp.objects.filter(email=self.data['email']).first()
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(obj_user)
        self.assertIsNone(temp)

    def test_valid_sent_response_if_temp_is_existed(self):
        initial_datetime = datetime.datetime.now()
        exam_data = {'email': 'example@gmail.com'}
        obj_user = User.objects.filter(**self.data).first()
        temp_example = Temp.objects.create(email= 'example@gmail.com')
        with freeze_time(initial_datetime) as frozen_datetime:
            frozen_datetime.tick()
            initial_datetime += datetime.timedelta(minutes=3)
            temp = Temp.objects.filter(**self.data).first()
            response = self.client.post(self.url, exam_data)
            self.assertIsNone(obj_user)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_User_is_existed(self):
        user = baker.make(User, **self.data)
        obj_user = User.objects.filter(**self.data).first()
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(obj_user)

    def test_time_expired_Temp(self):
        temp = baker.make(Temp, **self.data)
        response = self.client.post(self.url, self.data)
        temp_search = Temp.objects.filter(**self.data).first()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(temp_search)
        self.assertEqual(timezone.now() < temp.date + datetime.timedelta(minutes=2), True)
