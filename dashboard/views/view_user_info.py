from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from accounts.models import User, UserProject
from core.pagination import Pagination
from dashboard.filters import UserInfoFilter
from dashboard.serializers.serializer_user_info import UserInfoSerializer, UserBriefInfoSerializer
from dashboard.serializers.serializer_user_project import UserProjectSerializer


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

    def get_serializer_class(self):
        if self.action == 'list':
            return  UserBriefInfoSerializer
        return super(UserInfoView, self).get_serializer_class()



class UserInfoProjectView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = UserProjectSerializer
    queryset = UserProject.objects.filter(project__status__in=['STARTED', 'ENDED']).order_by(
        '-project__last_modified_date')

    def get_queryset(self):
        return self.queryset.filter(user__username=self.kwargs['slug_username'])

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
