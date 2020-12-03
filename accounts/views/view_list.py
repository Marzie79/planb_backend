from rest_framework import generics
from rest_framework.permissions import AllowAny

from accounts.serializers import *
from accounts.filters import ProvinceFilter, CityFilter, UniversityFilter


class SearchCity(generics.ListAPIView):
    serializer_class = CitySerializer
    permission_classes = (AllowAny,)
    filterset_class = CityFilter
    queryset = City.objects.all()


class SearchProvince(generics.ListAPIView):
    serializer_class = ProvinceSerializer
    permission_classes = (AllowAny,)
    filterset_class = ProvinceFilter
    queryset = Province.objects.all()


class SearchUniversity(generics.ListAPIView):
    serializer_class = UniversitySerializer
    permission_classes = (AllowAny,)
    filterset_class = UniversityFilter
    queryset = University.objects.all()
