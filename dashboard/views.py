from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import *
from accounts.views.view_profile import ProfileUser


class UserProjectView(viewsets.ReadOnlyModelViewSet):
    queryset = UserProject.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProjectSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


