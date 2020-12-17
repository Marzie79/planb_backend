from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
# don't use rest_framework.renderers.JsonRenderer !!!
from accounts.serializers import *
from core.exceptions import BadRequestError


def set_cookie_response(request):
    ser = MyTokenObtainPairSerializer(data=request.data,
                                      context={'request': request})
    try:
        ser.is_valid(raise_exception=True)
    except Exception as e:
        raise BadRequestError(e.args[0])
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
    create token cookie that save refresh in the value of cookie and send access token for authorization.
    """

    def post(self, request, *args, **kwargs):
        return set_cookie_response(request=request)


class MyTokenRefreshView(TokenRefreshView):
    """
       when is sent empty post , server send new access token if refresh(saves in the cookie) validate correctly.
    """
    serializer_class = TokenRefreshSerializer
    def post(self, request, *args, **kwargs):
        # get cookie and refresh token
        try:
            refresh = request.COOKIES['token']
            jwt_refresh = {'refresh': str(refresh)}
            ser = TokenRefreshSerializer(data=jwt_refresh)
            ser.is_valid(raise_exception=True)
        except Exception as e:
            raise InvalidToken(e.args[0])
        # create new access token
        # send access token
        return Response(ser.validated_data)


class Logout(generics.GenericAPIView):
    """
        token cookie will be deleted when user logs out.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = Response("logout user")
        response.delete_cookie('token')
        return response
