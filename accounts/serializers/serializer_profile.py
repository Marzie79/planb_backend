from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from accounts.models import *
from core.validators import FileSizeValidator, MAX_IMAGE_SIZE, MAX_FILE_SIZE
from .serializer_list import CitySerializer


class BriefProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
        'first_name', 'last_name', 'username','avatar')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
        'first_name', 'last_name', 'username', 'email', 'university', 'city', 'phone_number', 'description', 'gender')

    # def __init__(self, *args, **kwargs):
    #     super(ProfileSerializer, self).__init__(*args, **kwargs)
    #     request = self.context.get('request')
    #     if request and request.method=='patch':
    #         self.Meta.depth = 0
    #     else:
    #         self.Meta.depth = 1

class CityProfileSerializer(CitySerializer):
    from .serializer_list import ProvinceSerializer
    province = ProvinceSerializer()


class ProfileGetSerializer(ProfileSerializer):
    from .serializer_list import UniversitySerializer
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    city = CityProfileSerializer()
    university = UniversitySerializer()

    class Meta:
        model = User
        fields = ProfileSerializer.Meta.fields + ('gender_display',)


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
