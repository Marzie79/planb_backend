
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets, mixins, generics, filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from accounts.models import UserProject, NotificationToken, Project
from core.exceptions import BadRequestError
from core.helpers.main_helper import make_notification_and_message
from dashboard.filters import TeamProjectFilter
from core.helpers.make_message import make_message
from core.helpers.make_notification import make_notification
from dashboard.serializers.serializer_project_team import ProjectTeamSerializer


def get_update_text(name,status):
    message_status = _("accepted")
    text = _("Your requested joining to the {} project has been {}.").format(name, message_status)
    if status == "DECLINED":
        message_status = _("declined")
        text = _("Your requested joining to the {} project has been {}.").format(name, message_status)
    elif status == "DELETED":
        text = _("You have been removed from the {} project.").format(name)
    elif status == "ADMIN":
        text = _("You have become an admin for the {} project.").format(name)
    return text


class ProjectTeam(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = ProjectTeamSerializer
    filterset_class = TeamProjectFilter
    permission_classes = (DRYPermissions,)
    lookup_field = 'username'

    def get_permissions(self):
       # method = self.request.method
       # if method == 'GET' or method == 'PUT' or method == 'PATCH' or method == 'POST':
        return [DRYPermissions(), ]
       # return []

    def get_queryset(self):
        self.custom_check_permission()
        return UserProject.objects.filter(project__slug=self.kwargs['slug_slug']).order_by('status')

    def partial_update(self, request, *args, **kwargs):
        self.custom_check_permission()
        try:
            instance = UserProject.objects.select_related("project").get(user__username=self.kwargs['username'],
                                               project__slug=self.kwargs['slug_slug'])
        except UserProject.DoesNotExist:
            raise BadRequestError(_('ThisUserNotExist'))
        data = {'status': request.data['status']}
        previous_status = instance.status
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if request.data["status"] in ["DECLINED", "ACCEPTED", "DELETED", "ADMIN"]:
            if not (previous_status == "ADMIN" and request.data["status"] in ["ACCEPTED", "DELETED"]):
                text = get_update_text(instance.project.name,request.data['status'])

                make_notification_and_message(text, instance.project, recievers=[instance])
                # receivers_user = []
                # for item in [instance]:
                #     receivers_user.append(item.user)
                # recievers_token = list(NotificationToken.objects.filter(user__in=receivers_user).values_list('token'))
                # make_message(text=text, receiver= [instance], project= instance.project)
                # make_notification(recievers_token, instance.project.name, text)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        project = Project.objects.get(slug=self.kwargs['slug_slug'])
        request.data['project'] = project.pk
        request.data['user'] = request.user.id
        self.custom_check_permission()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        text = _("{} has requested to join the {} project.").format(self.request.user.__str__(),project.name)
        make_notification_and_message(text,project,statuses=["ADMIN", "CREATOR"])
        # receiver = UserProject.objects.filter(project=project).filter(status__in=["ADMIN", "CREATOR"])
        # recievers_user = []
        # for item in receiver:
        #     recievers_user.append(item.user)
        # recievers_token = list(NotificationToken.objects.filter(user__in=recievers_user).values_list('token', flat=True))
        # make_message(text=text, receiver= receiver, project= project)
        # make_notification(recievers_token, project.name, text)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def custom_check_permission(self):
        try:
            obj = UserProject.objects.get(Q(user=self.request.user) & Q(project__slug=self.kwargs['slug_slug']))
        except:
            obj = get_object_or_404(UserProject.objects.filter(project__slug=self.kwargs['slug_slug'])[:1])
        self.check_object_permissions(self.request, obj)
