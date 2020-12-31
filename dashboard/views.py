from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import *
from .filters import UserProjectFilter
from rest_framework import generics


class UserProjectView(viewsets.ReadOnlyModelViewSet):
    """
        Enter "PROJECT" or "REQUEST" as category,
        then you can also enter following items as status:
        for PROJECT --> WAITING, STARTED, ENDED, DELETED
        for REQUEST --> PENDING, DECLINED
    """
    queryset = UserProject.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProjectSerializer
    filterset_class = UserProjectFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        model = serializer.save()
        UserProject.objects.create(user=self.request.user,project=model,status='CREATOR')




# class CreateProjectView(generics.ListAPIView):
#     queryset = Project.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ProjectSerializer
#
#     def get_queryset(self):
#         return self.queryset.filter(creator=self.request.user)


