from drf_yasg.utils import swagger_auto_schema
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from accounts.models import Project, UserProject, NotificationToken
from core.helpers.main_helper import make_notification_and_message
from core.helpers.make_message import make_message
from core.helpers.make_notification import make_notification
from core.pagination import Pagination
from dashboard.filters import ProjectFilter
from dashboard.serializers.serializer_project import ProjectSaveSerializer, ProjectSerializer
from dashboard.serializers.serializer_user_project import ProjectStatusSerializer


class ProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('?')
    permission_classes = (DRYPermissions,)
    serializer_class = ProjectSaveSerializer
    filterset_class = ProjectFilter
    search_fields = ['name', 'category__name', 'skills__name']
    lookup_field = 'slug'
    pagination_class = Pagination

    def get_queryset(self):
        if self.action == 'list':
            return super(ProjectView, self).get_queryset().exclude(status="DELETED")
        return super(ProjectView, self).get_queryset()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProjectSerializer
        elif self.action == 'get_status':
            return ProjectStatusSerializer
        return super(ProjectView, self).get_serializer_class()

    def get_permissions(self):
        method = self.request.method
        if method == 'PATCH' or method == 'DELETE' or method == 'PUT' or method == 'POST':
            return [DRYPermissions(), ]
        return []

    def perform_create(self, serializer):
        model = serializer.save()
        UserProject.objects.create(user=self.request.user, project=model, status='CREATOR')

    def perform_update(self, serializer):
        instance=self.get_object()
        text = _("{} project information updated.").format(instance.name)
        make_notification_and_message(text, instance, statuses=["ADMIN", "CREATOR", "ACCEPTED"])
        # receiver = UserProject.objects.filter(project=instance).filter(status__in=["ADMIN", "CREATOR", "ACCEPTED"])
        # receivers_user = []
        # for item in receiver:
        #     receivers_user.append(item.user)
        # recievers_token = list(
        #     NotificationToken.objects.filter(user__in=receivers_user).values_list('token', flat=True))
        # make_message(text=text, receiver=receiver, project=instance)
        # make_notification(recievers_token, instance.name, text)

        if self.get_object().status == 'WAITING' and serializer.validated_data.get('status', None) and \
                serializer.validated_data['status'] == 'DELETED':
            self.get_object().delete()
        else:
            serializer.save()

    @action(methods=['get'], detail=True,
            url_path='status', url_name='get_status')
    @swagger_auto_schema(operation_description="""
   #User Statuses : 
    ACCEPTED ADMIN CREATOR : for members
    PENDING
    DECLINED
    DELETED

    #Project Statuses :
     WAITING
     STARTED
     ENDED
     DELETED
    """
                         )
    def get_status(self, request, slug=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
