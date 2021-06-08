from django_filters import rest_framework as filters
from accounts.models import Province, City, University

class ProvinceFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name")
    code = filters.CharFilter(field_name="code")

    class Meta:
        model: Province
        fields = ['code','name']


class CityFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name")
    code = filters.CharFilter(field_name="code")
    province = filters.NumberFilter(field_name="province__id")

    class Meta:
        model: City
        fields = ['code','name','province']


class UniversityFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name")
    code = filters.CharFilter(field_name="code")
    city = filters.NumberFilter(field_name="city__id")

    class Meta:
        model: University
        fields = ['code','name','city']


class SkillFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name")
    code = filters.CharFilter(field_name="code")
    skill = filters.NumberFilter(field_name="skill__id")
    all = filters.BooleanFilter(method='get_all')

    class Meta:
        model: University
        fields = ['code', 'name', 'skill']

    def get_all(self, queryset, name, value):
        if not value:
             return queryset.filter(skill__isnull=True)
        return queryset