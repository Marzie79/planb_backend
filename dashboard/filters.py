from django_filters import rest_framework as filters
from accounts.models import UserProject


class UserProjectFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=UserProject.STATUS_CHOICES)

    class Meta:
        model: UserProject
        fields = ['status', ]