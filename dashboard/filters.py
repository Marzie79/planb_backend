from django_filters import rest_framework as filters
from accounts.models import UserProject

# DELETED,STARTED,ENDED,ACCEPTED,REQUESTED
class UserProjectFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=UserProject.STATUS_CHOICES)

    class Meta:
        model: UserProject
        fields = ['status', ]