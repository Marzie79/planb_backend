from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.models import UserProject
from dashboard.filters import UserProjectFilter
from dashboard.serializers.serializer_user_project import UserProjectSerializer


class UserProjectView(generics.ListAPIView):
    """
        Enter "PROJECT" or "REQUEST" as category,
        then you can also enter following items as status:
        for PROJECT --> WAITING, STARTED, ENDED, DELETED
        for REQUEST --> PENDING, DECLINED
    """
    queryset = UserProject.objects.all().order_by('-project__last_modified_date')
    serializer_class = UserProjectSerializer
    filterset_class = UserProjectFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)