import sys

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
# don't use rest_framework.renderers.JsonRenderer !!!
from accounts.enums import *
from accounts.serializers import *
from accounts.views.view_token import set_cookie_response
from core.exceptions import BadRequestError, ServerError
from core.utils import EmailUtils
from rest_framework.exceptions import server_error
import datetime


class SignUp(generics.GenericAPIView):
    """
        get just user's email for sending link to verify email.
    """
    serializer_class = SignUpEmailSerializer
    renderer_classes = [CamelCaseJSONRenderer]

    def post(self, request):
        return send_email(request, True)


class VerifyAccount(viewsets.ModelViewSet):
    filter_backends = None

    def get_serializer_class(self):
        if self.action == 'list':
            return TempSerializer
        else:
            return SignUpSerializer

    test_param = openapi.Parameter('code', openapi.IN_QUERY, description="unique code in url.",
                                   type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[test_param, ],
                         operation_description="user click on a link and you should get code from it and send code for server.\n\r use in : 1. verify email 2. reset password.")
    def retrieve(self, request, *args, **kwargs):
        serialize = TempSerializer(get_object_or_404(Temp, code=request.GET.get('code')))
        # check that user send correct data
        if serialize.is_valid:
            # send email and code for making a user and removing temp object
            return Response(data=serialize.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
            user's email have been validate and we want to get other necessary fields.
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


class ResetPassword(viewsets.ModelViewSet):
    """
        write the code that you get before from server and enter new password.
    """

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ResetPasswordSerializer
        else:
            return SignUpEmailSerializer

    def partial_update(self, request, *args, **kwargs):
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

    def create(self, request, *args, **kwargs):
        return send_email(request, False)


def send_email(request, is_obj_user):
    serializer = SignUpEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # check that this email try to signup or not
    obj = Temp.objects.filter(email=serializer.data['email']).first()
    # check this email signup before or not
    obj_user = User.objects.filter(email=serializer.data['email']).first()
    if not is_obj_user:
        if not obj_user:
            raise BadRequestError(_("User_Email_Error"))
    else:
        if obj_user:
            raise BadRequestError(_("EmailDoesExist"))

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
            raise BadRequestError(_("EmailTimeError"))
    else:
        obj = Temp.objects.create(email=serializer.data['email'], date=time_now,
                                  code=get_random_string(length=16))

    if 'Origin' in request.headers:
        if not is_obj_user:
            url = request.headers['Origin'] + FrontURL.FORGET_PASSWORD.value + obj.code
        else:
            url = request.headers['Origin'] + FrontURL.SIGNUP.value + obj.code
    else:
        if not is_obj_user:
            url = FrontURL.ROOT.value + FrontURL.FORGET_PASSWORD.value + obj.code
        else:
            url = FrontURL.ROOT.value + FrontURL.SIGNUP.value + obj.code

    if not 'test' in sys.argv:
        message = EmailUtils.sending_email(validation=url, receiver=obj.email)
        if message is not None:
            obj.delete()
            raise ServerError(_("ServerError"))
    return Response(status=status.HTTP_200_OK)
