from django_filters import rest_framework as filters
from accounts.models import Province, City, University

class ProvinceFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="name")
    code = filters.NumberFilter(field_name="code")

    class Meta:
        model: Province
        fields = ['code','name']


class CityFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="name")
    code = filters.NumberFilter(field_name="code")
    province = filters.NumberFilter(field_name="province__id")

    class Meta:
        model: City
        fields = ['code','name','province']


class UniversityFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="name")
    code = filters.NumberFilter(field_name="code")
    city = filters.NumberFilter(field_name="city__id")

    class Meta:
        model: University
        fields = ['code','name','city']