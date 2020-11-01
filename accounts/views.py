import datetime
import coreapi
# import requests
from abc import ABC
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.db.models import Q
from django.contrib.auth.backends import BaseBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
# from rest_framework.views import APIView
# from rest_framework.utils import json
from accounts.serializers import *
from accounts.util import sending_email
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


def set_cookie_response(request, username, password):
    ser = MyTokenObtainPairSerializer()
    # make jwt token
    jwt_token = ser.validate({'username': username, 'password': password})
    access_token = {'access': jwt_token['access']}
    # put access token on response
    response = Response(access_token)
    # create cookie and save refresh token on value and set http only flag
    response.set_cookie("token", jwt_token['refresh'], httponly=True,
                        expires=datetime.datetime.now() + datetime.timedelta(days=180))
    return response


# create token and use this view as login view
class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        return set_cookie_response(request=request, username=request.data['username'],
                                   password=request.data['password'])


class MyTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            ser = TokenRefreshSerializer()
            # get cookie and refresh token
            refresh = request.COOKIES['token']
            jwt_refresh = {'refresh': str(refresh)}
            # create new access token
            jwt_token = {'access': ser.validate(jwt_refresh)}
            # send access token
            return Response(jwt_token['access'])
        except:
            return Response({'error': 'you should login again'}, status=status.HTTP_401_UNAUTHORIZED)


class SimpleFilterBackend(BaseFilterBackend, ABC):
    def get_schema_fields(self, view):
        return [coreapi.Field(name='code', location='query', required=False, type='string')]


class SignUp(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpEmailSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def post(self, request):
        serializer = SignUpEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # check that this email try to signup or not before
        obj = Temp.objects.filter(email=serializer.data['email']).first()
        # check this email signup before or not
        obj_user = User.objects.filter(email=serializer.data['email']).first()
        if obj_user:
            return Response(status=status.HTTP_409_CONFLICT, data={'error': 'حسابی با این ایمیل موجود می باشد.'})
        time_now = timezone.now()
        # check this email have request before for signup or not
        if obj:
            # check that this email dont have request in this 2 minutes
            if time_now > obj.date + datetime.timedelta(minutes=2):
                # make a random string for making a unique url
                obj.code = get_random_string(length=16)
                obj.date = time_now
                obj.save()
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={
                    'error': 'در دو دقیقه اخیر ایمیلی به این حساب کاربری ارسال شده است لطفا مجددا تلاش فرمایید.'})

        else:
            obj = Temp.objects.create(email=serializer.data['email'], date=time_now,
                                      code=get_random_string(length=16))

        url = request.build_absolute_uri('/') + 'api/v1/validate-email/?code=' + obj.code
        message = sending_email(validation=url, receiver=obj.email)
        if message is not None:
            obj.delete()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            data={'message': 'خطایی رخ داده است لطفا دوباره امتحان کنید.'})
        return Response(status=status.HTTP_200_OK, template_name='build/index.html')


class ValidateEmail(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)

    # filter_backends = (SimpleFilterBackend,)
    def get_serializer_class(self):
        if self.action == 'list':
            return TempSerializer
        else:
            return SignUpSerializer

    test_param = openapi.Parameter('code', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[test_param, ], operation_description="partial_update description override")
    def list(self, request, *args, **kwargs):
        serialize = TempSerializer(get_object_or_404(Temp, code=request.GET.get('code')))
        # check that user send correct data
        if serialize.is_valid:
            # send email and code for making a user and removing temp object
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'لینک وارد شده نامعتبر است.'})

    def create(self, request, *args, **kwargs):
        # if User.objects.filter(username=request.data['username']).first():
        #     return Response(status=status.HTTP_100_CONTINUE)

        serialize = SignUpSerializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        # check that code is exist
        obj = get_object_or_404(Temp, code=serialize.data.get('temp').get('code'))
        obj.delete()
        # make a new user
        user = UserSerializer(data=serialize.data['user'])
        user.is_valid(raise_exception=True)
        user.save()
        # send token of user
        return set_cookie_response(request, username=request.data['user.username'],
                                   password=request.data['user.password'])


# make authenticate with username and email
class UsernameOrEmailBackend(BaseBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        # Try to fetch the user by searching the username or email field
        user = get_object_or_404(User, Q(email=username) | Q(username=username))
        if user.check_password(password):
            return user
        # a user with this email or password not exist
        else:
            return None


class SignIn(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user_set = UsernameOrEmailBackend().authenticate(username=serializer.data['username'],
                                                             password=serializer.data['password'])
            if user_set is not None:
                # everything is ok
                token, created = Token.objects.get_or_create(user=user_set)
                return Response(data={'token': token.key}, status=status.HTTP_200_OK)
            else:
                # password in not correct
                return Response(data={'error': 'نام کاربری یا رمز عبور اشتباه است'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        # sending empty request
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RequestResetPassword(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpEmailSerializer

    def post(self, request):
        serializer = SignUpEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # check that this email try to signup or not
        obj = Temp.objects.filter(email=serializer.data['email']).first()
        # check this email signup before or not
        obj_user = User.objects.filter(email=serializer.data['email']).first()
        if not obj_user:
            return Response(status=status.HTTP_409_CONFLICT, data={'error': 'کاربری با این ایمیل موجود نمی‌باشد.'})
        time_now = timezone.now()
        # check this email have request before for signup or not
        if obj:
            # check that this email dont have request in this 2 minutes
            if time_now > obj.date + datetime.timedelta(minutes=2):
                # make a random string for making a unique url
                obj.code = get_random_string(length=16)
                obj.date = time_now
                obj.save()
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={
                    'error': 'در دو دقیقه اخیر ایمیلی به این حساب کاربری ارسال شده است لطفا مجددا تلاش فرمایید.'})
        else:
            obj = Temp.objects.create(email=serializer.data['email'], date=time_now,
                                      code=get_random_string(length=16))

        url = request.build_absolute_uri('/') + 'api/v1/reset-password/?code=' + obj.code
        message = sending_email(validation=url, receiver=obj.email)
        if message is not None:
            obj.delete()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            data={'message': 'خطایی رخ داده است لطفا دوباره امتحان کنید.'})
        return Response(status=status.HTTP_200_OK)


class ResetPassword(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer
    filter_backends = (SimpleFilterBackend,)

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        get_object_or_404(Temp, code=serializer.data.get('temp').get('code')).delete()
        # get user for setting new password
        obj_user = get_object_or_404(User, email=serializer.data.get('temp').get('email'))
        obj_user.set_password(serializer.data['password'])
        obj_user.save()
        # get or create token of user
        # send token of user
        return set_cookie_response(request, username=obj_user.username, password=request.data['password'])

# class GoogleView(APIView):
#     def post(self, request):
#         payload = {'access_token': request.data.get("token")}  # validate the token
#         r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
#         data = json.loads(r.text)
#
#         if 'error' in data:
#             content = {'message': 'wrong google token / this google token is already expired.'}
#             return Response(content)
#
#         # create user if not exist
#         try:
#             user = User.objects.get(email=data['email'])
#         except User.DoesNotExist:
#             user = User()
#             user.email = data['email']
#
#         token = 'rnfbvksdlbm'  # generate token without username & password
#         response = {}
#         response['username'] = user.username
#         response['access_token'] = str(token)
#         response['refresh_token'] = str(token)
#         return Response(response)
