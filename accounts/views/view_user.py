from accounts.serializers.serializer_user import *
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import viewsets, mixins, generics


class UserInfoView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    lookup_field = 'username'
    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return GetUserInfoSerializer
    #     return self.serializer_class
    