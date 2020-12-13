import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import *

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # regex for email validator
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, attrs['username']):
            user = User.objects.get(email=attrs['username'])
            attrs['username'] = user.username
        # return access and refresh token
        return super().validate(attrs)
