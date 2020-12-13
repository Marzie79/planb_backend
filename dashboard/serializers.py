from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from accounts.models import *


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class UserSkillSerializer(serializers.ModelSerializer):
    skills = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'skills',)

    def get_skills(self, instance):
        skills = instance.skills.order_by('name')
        return SkillSerializer(skills, many=True).data


class UpdateSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'skills',)
