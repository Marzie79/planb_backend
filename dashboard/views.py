import random

from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from dry_rest_permissions.generics import DRYPermissions

from rest_framework import viewsets, mixins, generics, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.pagination import Pagination
from .serializers import *
from .filters import UserProjectFilter, TeamProjectFilter, UserInfoFilter
from core.helpers.make_message import make_message
from core.helpers.make_notification import make_notification

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


class ProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('?')
    permission_classes = (DRYPermissions,)
    serializer_class = ProjectSaveSerializer
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
        if self.get_object().status =='WAITING' and serializer.validated_data.get('status',None) and serializer.validated_data['status']=='DELETED':
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
        text = "اطلاعات پروژه %s به روز رسانی شد."%(instance.name)
        receiver = UserProject.objects.filter(project=instance).filter(status__in=["ADMIN", "CREATOR", "ACCEPTED"])
        receivers_user = []
        for item in receiver:
            receivers_user.append(item.user)
        recievers_token = list(NotificationToken.objects.filter(user__in=receivers_user).values_list('token', flat=True))
        make_message(text=text, receiver= receiver, project= instance)
        make_notification(recievers_token, instance.name, text)
        return Response(serializer.data)


class ProjectTeam(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = ProjectTeamSerializer
    filterset_class = TeamProjectFilter
    permission_classes = (DRYPermissions,)
    lookup_field = 'username'

    def get_permissions(self):
        method = self.request.method
        if method == 'GET' or method == 'PUT' or method == 'PATCH' or method == 'POST':
            return [DRYPermissions(), ]
        return []

    def get_queryset(self):
        self.custom_check_permission()
        return UserProject.objects.filter(project__slug=self.kwargs['slug_slug']).order_by('status')

    def partial_update(self, request, *args, **kwargs):
        self.custom_check_permission()
        try:
            instance = UserProject.objects.select_related("project").get(user__username=self.kwargs['username'],
                                               project__slug=self.kwargs['slug_slug'])
        except UserProject.DoesNotExist:
            return Response(data={"bad_request": _('ThisUserNotExist')})
        data = {'status': request.data['status']}
        previous_status = instance.status
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if request.data["status"] in ["DECLINED", "ACCEPTED", "DELETED", "ADMIN"]:
            if not (previous_status == "ADMIN" and request.data["status"] in ["ACCEPTED", "DELETED"]):
                message_status = "قبول"
                text = "درخواست شما برای پیوستن به پروژه %s %s شده است."%(instance.project.name, message_status)
                if request.data["status"] == "DECLINED":
                    message_status = "رد"
                    text = "درخواست شما برای پیوستن به پروژه %s %s شده است."%(instance.project.name, message_status)
                elif request.data["status"] == "DELETED":
                    text = "شما از پروژه %s حذف شدید."%instance.project.name
                elif request.data["status"] == "ADMIN":
                    text = "شما ادمین پروژه %s شدید."%instance.project.name
                receivers_user = []
                for item in [instance]:
                    receivers_user.append(item.user)
                recievers_token = list(NotificationToken.objects.filter(user__in=receivers_user).values_list('token'))
                make_message(text=text, receiver= [instance], project= instance.project)
                make_notification(recievers_token, instance.project.name, text)
        
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.custom_check_permission()
        project = Project.objects.get(slug=self.kwargs['slug_slug'])
        request.data['project'] = project.pk
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        text = "%s درخواست پیوستن به پروژه %s را دارد."%(self.request.user.__str__(),project.name)
        receiver = UserProject.objects.filter(project=project).filter(status__in=["ADMIN", "CREATOR"])
        recievers_user = []
        for item in receiver:
            recievers_user.append(item.user)
        recievers_token = list(NotificationToken.objects.filter(user__in=recievers_user).values_list('token', flat=True))
        make_message(text=text, receiver= receiver, project= project)
        make_notification(recievers_token, project.name, text)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def custom_check_permission(self):
        try:
            obj = UserProject.objects.get(Q(user=self.request.user) & Q(project__slug=self.kwargs['slug_slug']))
        except:
            obj = get_object_or_404(UserProject.objects.filter(project__slug=self.kwargs['slug_slug'])[:1])
        self.check_object_permissions(self.request, obj)


class UserInfoView(viewsets.ReadOnlyModelViewSet):
    """
       #User Statuses :
        CREATOR OTHER
        """
    filterset_class = UserInfoFilter
    search_fields = ['username', 'skills__name']

    queryset = User.objects.all().distinct()
    serializer_class = UserInfoSerializer
    lookup_field = 'username'
    pagination_class = Pagination

class UserInfoProjectView(mixins.ListModelMixin,GenericViewSet):
    serializer_class = UserProjectSerializer
    queryset = UserProject.objects.filter(project__status__in=['STARTED','ENDED']).order_by('-project__last_modified_date')

    def get_queryset(self):
        return self.queryset.filter(user__username=self.kwargs['slug_username'])



class MessageView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    pagination_class = Pagination

    def get_queryset(self):
        return Message.objects.filter(reciever__user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        recievers = Reciever.objects.filter(message__in=page).filter(user=request.user)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            recievers.update(is_visited=True)
            return result
        serializer = self.get_serializer(queryset, many=True)
        recievers.update(is_visited=True)
        return Response(serializer.data)


class NotificationView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = NotificationToken.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return NotificationToken.objects.filter(user=self.request.user)


    
# class UsersList(generics.ListAPIView):
#     queryset = User.objects.exclude(userproject__status='CREATOR').distinct()
#     serializer_class = PersonSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['username', 'skills__name']
#     pagination_class = Pagination
#
#
# class CreatorsList(generics.ListAPIView):
#     queryset = User.objects.filter(userproject__status='CREATOR').distinct()
#     serializer_class = PersonSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['username', 'skills__name']
#     pagination_class = Pagination


# class CreateProjectView(generics.ListAPIView):
#     queryset = Project.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ProjectSerializer
#
#     def get_queryset(self):
#         return self.queryset.filter(creator=self.request.user)
