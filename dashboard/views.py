from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins
from .serializers import *
from accounts.views.view_profile import ProfileUser


class UserProject(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = UserProject.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProjectSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
