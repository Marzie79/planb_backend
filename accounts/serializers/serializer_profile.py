from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from accounts.models import *
from core.validators import FileSizeValidator, MAX_IMAGE_SIZE, MAX_FILE_SIZE


class ProfileSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'university', 'city', 'phone_number', 'description','gender','gender_display')


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar',)
        validators = [
            FileSizeValidator(
                size=MAX_IMAGE_SIZE,
            )
        ]


class ProfileResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('resume',)
        validators = [
            FileSizeValidator(
                size=MAX_FILE_SIZE,
            )
        ]

class UpdateSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('skills',)


class UserSkillSerializer(UpdateSkillSerializer):
    skills = SerializerMethodField()

    def get_skills(self, instance):
        from accounts.serializers import SkillBriefSerializer
        skills = instance.skills.order_by('name')
        return SkillBriefSerializer(skills, many=True).data



