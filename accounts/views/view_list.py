from rest_framework import generics

from accounts.serializers import *
from accounts.filters import ProvinceFilter, CityFilter, UniversityFilter, SkillFilter


class SearchCity(generics.ListAPIView):
    serializer_class = CitySerializer
    filterset_class = CityFilter
    queryset = City.objects.all()


class SearchProvince(generics.ListAPIView):
    serializer_class = ProvinceSerializer
    filterset_class = ProvinceFilter
    queryset = Province.objects.all()


class SearchUniversity(generics.ListAPIView):
    serializer_class = UniversitySerializer
    filterset_class = UniversityFilter
    queryset = University.objects.all()


class SearchSkill(generics.ListAPIView):
    serializer_class = SkillSerializer
    filterset_class = SkillFilter
    queryset = Skill.objects.all()

    def get_queryset(self):
        if self.request.META['QUERY_STRING']:
            return super(SearchSkill, self).get_queryset()
        return Skill.objects.filter(skill__isnull=True)
