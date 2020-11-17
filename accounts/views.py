import coreapi
from abc import ABC
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.backends import BaseBackend
from django.utils.translation import gettext_lazy as _

from rest_framework import status, generics, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
# don't use rest_framework.renderers.JsonRenderer !!!

from accounts.serializers import *
from core.util import sending_email
import datetime


def set_cookie_response(request):
    ser = MyTokenObtainPairSerializer(data=request.data,
                                      context={'request': request})
    ser.is_valid(raise_exception=True)
    jwt_token = ser.validated_data
    # make jwt token
    access_token = {'access': jwt_token['access']}
    # put access token on response
    response = Response(access_token)
    # create cookie and save refresh token on value and set http only flag
    response.set_cookie("token", jwt_token['refresh'], httponly=True,
                        expires=timezone.now() + timezone.timedelta(days=180))
    return response


# create token and use this view as login view
class MyTokenObtainPairView(TokenObtainPairView):
    """
    create token cookie that save refresh in the value of cookie and send access token for authorization
    """

    def post(self, request, *args, **kwargs):
        return set_cookie_response(request=request)


class MyTokenRefreshView(TokenRefreshView):
    """
       when is sent empty post , server send new access token if refresh(saves in the cookie) validate correctly
    """

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


class Logout(generics.GenericAPIView):
    """
        token cookie will be deleted when user logs out
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = Response("logout user")
        response.delete_cookie('token')
        return response


class SignUp(generics.GenericAPIView):
    """
        get just user's email for sending link to verify email
    """
    permission_classes = (AllowAny,)
    serializer_class = SignUpEmailSerializer
    renderer_classes = [TemplateHTMLRenderer, CamelCaseJSONRenderer]

    def post(self, request):
        serializer = SignUpEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # check that this email try to signup or not before
        obj = Temp.objects.filter(email=serializer.data['email']).first()
        # check this email signup before or not
        obj_user = User.objects.filter(email=serializer.data['email']).first()
        if obj_user:
            return Response(status=status.HTTP_409_CONFLICT, data={'error': _("EmailDoesExist")})
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
                    'error': "EmailTimeError"})

        else:
            obj = Temp.objects.create(email=serializer.data['email'], date=time_now,
                                      code=get_random_string(length=16))

        url = request.build_absolute_uri('/') + 'api/v1/validate-email/?code=' + obj.code
        message = sending_email(validation=url, receiver=obj.email)
        if message is not None:
            obj.delete()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            data={'message': _("ServerError")})
        return Response(status=status.HTTP_200_OK, template_name='build/index.html')


class VerifyAccount(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    filter_backends = None

    def get_serializer_class(self):
        if self.action == 'list':
            return TempSerializer
        else:
            return SignUpSerializer

    test_param = openapi.Parameter('code', openapi.IN_QUERY, description="unique code in url", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[test_param, ], operation_description="user click on this field and you should get it and send it for server"
                                                                                 "use in : 1. verify email for password 2. reset password")
    def list(self, request, *args, **kwargs):
        serialize = TempSerializer(get_object_or_404(Temp, code=request.GET.get('code')))
        # check that user send correct data
        if serialize.is_valid:
            # send email and code for making a user and removing temp object
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': _("InValidLink")})

    def create(self, request, *args, **kwargs):
        """
            user's email have been validate and we want to get other necessary fields
        """
        serialize = SignUpSerializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        # check that code is exist
        obj = get_object_or_404(Temp, code=serialize.data.get('temp').get('code'))
        obj.delete()
        # make a new user
        user = UserSerializer(data=serialize.data['user'])
        user.is_valid(raise_exception=True)
        user.save()
        request.data['username'] = serialize.data.get('user').get('username')
        request.data['password'] = serialize.data.get('user').get('password')
        # send token of user
        return set_cookie_response(request)


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
                return Response(data={'error': _("UsernameOrPasswordWrong")},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        # sending empty request
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RequestResetPassword(generics.GenericAPIView):
    """
        get just user's email for sending a link for changing password
    """
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
            return Response(status=status.HTTP_409_CONFLICT, data={'error': _("User_Email_Error")})
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
                    'error': _("EmailTimeError")})
        else:
            obj = Temp.objects.create(email=serializer.data['email'], date=time_now,
                                      code=get_random_string(length=16))

        url = request.build_absolute_uri('/') + 'api/v1/reset-password/?code=' + obj.code
        message = sending_email(validation=url, receiver=obj.email)
        if message is not None:
            obj.delete()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            data={'message': _("ServerError")})
        return Response(status=status.HTTP_200_OK)


class ResetPassword(generics.GenericAPIView):
    """
        save the new password of user
    """
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer
    filter_backends = (SimpleFilterBackend,)

    def patch(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # get user for setting new password
        temp_obj = get_object_or_404(Temp, code=serializer.data.get('temp').get('code'))
        obj_user = get_object_or_404(User, email=temp_obj.email)
        temp_obj.delete()
        obj_user.set_password(serializer.data['password'])
        obj_user.save()
        request.data['username'] = obj_user.username
        # send token of user
        return set_cookie_response(request)


class SearchCity(generics.ListAPIView):
    serializer_class = CitySerializer
    permission_classes = (AllowAny,)
    search_fields = ('province__id', 'name')
    queryset = City.objects.all()


class SearchProvince(generics.ListAPIView):
    serializer_class = ProvinceSerializer
    permission_classes = (AllowAny,)
    search_fields = ('code', 'name')
    queryset = Province.objects.all()


class SearchUniversity(generics.ListAPIView):
    serializer_class = UniversitySerializer
    permission_classes = (AllowAny,)
    search_fields = ('code', 'name', 'city__id')
    queryset = University.objects.all()


class ProfileUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return self.request.user
