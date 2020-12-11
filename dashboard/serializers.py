from rest_framework import serializers
from accounts.models import *


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class UserSkillSerializer(serializers.ModelSerializer):
    skills = serializers.ReadOnlyField(source='name')

    class Meta:
        model = User
        fields = ('id', 'skills',)


class ChildSkillSerializer(serializers.ModelSerializer):
    skill = serializers.ReadOnlyField(source='name')

    class Meta:
        model = Skill
        fields = ('id', 'skill',)
