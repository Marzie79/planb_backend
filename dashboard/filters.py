from django_filters import rest_framework as filters
from accounts.models import UserProject, Project
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
            return queryset.filter(status='ACCEPTED')
        elif value == "REQUEST":
            return queryset.filter(Q(status='PENDING') | Q(status='DECLINED'))

    def get_status(self, queryset, name, value):
        if self.data['category'] == "PROJECT":
            return queryset.filter(project__status=value)
        elif self.data['category'] == "REQUEST":
            return queryset.filter(status=value)
