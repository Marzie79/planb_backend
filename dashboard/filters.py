from django_filters import rest_framework as filters
from accounts.models import UserProject, Project, User
from django.db.models import Q


# DELETED,STARTED,ENDED,ACCEPTED,REQUESTED
class UserProjectFilter(filters.FilterSet):
    CATEGORY_CHOICES = (
        ('PROJECT', 'project'),
        ('REQUEST', 'request'),
    )
    category = filters.ChoiceFilter(choices=CATEGORY_CHOICES, method='get_category')
    status = filters.ChoiceFilter(choices=(UserProject.STATUS_CHOICES + Project.STATUS_CHOICES), method='get_status')

    class Meta:
        model: UserProject
        fields = ['status', ]

    """Display accepted projects when category is null"""

    def __init__(self, data, *args, **kwargs):
        if not data.get('category'):
            data = data.copy()
            data['category'] = 'PROJECT'
        super().__init__(data, *args, **kwargs)

    def get_category(self, queryset, name, value):
        if value == "PROJECT":
            return queryset.filter(Q(status='ACCEPTED') | Q(status='ADMIN') | Q(status='CREATOR'))
        elif value == "REQUEST":
            return queryset.filter(Q(status='PENDING') | Q(status='DECLINED'))

    def get_status(self, queryset, name, value):
        if self.data['category'] == "PROJECT":
            return queryset.filter(project__status=value)
        elif self.data['category'] == "REQUEST":
            return queryset.filter(status=value)


class TeamProjectFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=(UserProject.STATUS_CHOICES + Project.STATUS_CHOICES), method='get_status')

    class Meta:
        model: UserProject
        fields = ['status', ]

    def __init__(self, data, *args, **kwargs):
        if not data.get('status'):
            data = data.copy()
            data['status'] = 'ACCEPTED'
        super().__init__(data, *args, **kwargs)

    def get_status(self, queryset, name, value):
        if value == 'ACCEPTED':
            return queryset.filter(Q(status='ACCEPTED') | Q(status='ADMIN') | Q(status='CREATOR'))
        elif value == 'PENDING':
            return queryset.filter(Q(status='Pending'))


class UserInfoFilter(filters.FilterSet):
    university = filters.NumberFilter(field_name="university__id")
    skill = filters.NumberFilter(field_name="skill__id")
    city = filters.NumberFilter(field_name="city__id")
    province = filters.NumberFilter(field_name="city__province__id")
    USER_CATEGORY_CHOICES = (
        ('CREATOR', 'creator'),
        ('OTHER', 'other'),
    )
    status = filters.ChoiceFilter(choices=USER_CATEGORY_CHOICES,method='get_status')

    class Meta:
        model: User
        fields = ['status', ]

    def get_status(self, queryset, name, value):
        if value:
            if value == "CREATOR":
                return queryset.filter(userproject__status='CREATOR')
            return queryset.exclude(userproject__status='CREATOR')
        return queryset


class ProjectFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=(Project.STATUS_CHOICES))
    category = filters.NumberFilter(field_name="category_id")
    skill = filters.NumberFilter(field_name="skills")