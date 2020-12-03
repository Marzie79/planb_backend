from django.utils import timezone
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
# don't use rest_framework.renderers.JsonRenderer !!!
from accounts.serializers import *


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
    create token cookie that save refresh in the value of cookie and send access token for authorization.
    """

    def post(self, request, *args, **kwargs):
        return set_cookie_response(request=request)


class MyTokenRefreshView(TokenRefreshView):
    """
       when is sent empty post , server send new access token if refresh(saves in the cookie) validate correctly.
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


class Logout(generics.GenericAPIView):
    """
        token cookie will be deleted when user logs out.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = Response("logout user")
        response.delete_cookie('token')
        return response
