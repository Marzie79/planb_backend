import re
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueForYearValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext as _
from accounts.models import *
from core.validators import FileSizeValidator, MAX_IMAGE_SIZE, MAX_FILE_SIZE


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id' , 'code', 'name')


class CitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()

    class Meta:
        model = City
        fields = ('id', 'code', 'name', 'province')


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('id', 'code', 'name', 'city')


class SkillBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class SkillSerializer(SkillBriefSerializer):
    class Meta:
        model = Skill
        fields = SkillBriefSerializer.Meta.fields + ('code', 'skill','image')

