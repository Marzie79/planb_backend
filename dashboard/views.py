from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from dry_rest_permissions.generics import DRYPermissions

from rest_framework import viewsets, mixins, generics
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import *
from .filters import UserProjectFilter, TeamProjectFilter


class UserProjectView(generics.ListAPIView):
    """
        Enter "PROJECT" or "REQUEST" as category,
        then you can also enter following items as status:
        for PROJECT --> WAITING, STARTED, ENDED, DELETED
        for REQUEST --> PENDING, DECLINED
    """
    queryset = UserProject.objects.all()
    serializer_class = UserProjectSerializer
    filterset_class = UserProjectFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = (DRYPermissions,)
    serializer_class = ProjectSaveSerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProjectSerializer
        return super(ProjectView, self).get_serializer_class()

    def get_permissions(self):
        if self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return [DRYPermissions(), ]
        return []

    def perform_create(self, serializer):
        model = serializer.save()
        UserProject.objects.create(user=self.request.user, project=model, status='CREATOR')

    @action(methods=['get'], detail=True,
            url_path='status', url_name='get_status')
    @swagger_auto_schema(operation_description="""
   # Statuses : 
    ACCEPTED ADMIN CREATOR : for members
    PENDING
    DECLINED
    DELETED
    """
    )
    def get_status(self, request, slug=None):
        instance = self.get_object()
        serializer = StatusSerializer(instance)
        return Response(serializer.data)


class ProjectTeam(mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = ProjectTeamSerializer
    filterset_class = TeamProjectFilter
    permission_classes = (DRYPermissions,)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [DRYPermissions(), ]
        return []

    def get_queryset(self):
        obj = get_object_or_404(
            UserProject.objects.filter(Q(user=self.request.user) & Q(project__slug=self.kwargs['slug_slug'])))
        self.check_object_permissions(self.request, obj)
        return UserProject.objects.filter(project__slug=self.kwargs['slug_slug'])

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = UserProject.objects.get(pk=self.kwargs['pk'])
        except UserProject.DoesNotExist:
            return Response(data={"bad_request": _('ThisUserNotExist')})
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

# class CreateProjectView(generics.ListAPIView):
#     queryset = Project.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ProjectSerializer
#
#     def get_queryset(self):
#         return self.queryset.filter(creator=self.request.user)
