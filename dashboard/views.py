from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .filters import UserProjectFilter, TeamProjectFilter


class UserProjectView(viewsets.ReadOnlyModelViewSet):
    """
        Enter "PROJECT" or "REQUEST" as category,
        then you can also enter following items as status:
        for PROJECT --> WAITING, STARTED, ENDED, DELETED
        for REQUEST --> PENDING, DECLINED
    """
    queryset = UserProject.objects.all()
    serializer_class = UserProjectSerializer
    filterset_class = UserProjectFilter
    lookup_field = 'project__slug'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        model = serializer.save()
        UserProject.objects.create(user=self.request.user, project=model, status='CREATOR')


class ProjectTeam(viewsets.ModelViewSet):
    """
    make a json like this:
    {
    "status": "ACCEPTED",
    "id": 305
    }
    """
    serializer_class = ProjectTeamSerializer
    filterset_class = TeamProjectFilter
    queryset = UserProject.objects.all()
    lookup_field = 'slug'

    def get_queryset(self):
        return UserProject.objects.filter(project__slug=self.kwargs['slug'])

    def update(self, request, *args, **kwargs):
        try:
            instance = UserProject.objects.get(pk=request.data['id'])
        except UserProject.DoesNotExist:
            return Response(data={"bad_request": _('ThisUserNotExist')})
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

# class CreateProjectView(generics.ListAPIView):
#     queryset = Project.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ProjectSerializer
#
#     def get_queryset(self):
#         return self.queryset.filter(creator=self.request.user)
