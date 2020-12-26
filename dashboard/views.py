from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import *
from .filters import UserProjectFilter


class UserProjectView(viewsets.ReadOnlyModelViewSet):
    """
        Enter "PROJECT" or "PENDING" as category,
        then you can also enter following items as status:
        for PROJECT --> WAITING, STARTED, ENDED, DELETED
        for PENDING --> REQUESTED, DECLINED
    """
    queryset = UserProject.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProjectSerializer
    filterset_class = UserProjectFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CreateProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateProjectSerializer
    
    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)


