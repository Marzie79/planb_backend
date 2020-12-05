import re
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext as _
from accounts.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ResetPasswordUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class TempSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temp
        fields = ('code', 'email')
        extra_kwargs = {'email': {'read_only': True}}


class SignUpSerializer(serializers.Serializer):
    temp = TempSerializer()
    user = UserSerializer()


class ResetPasswordSerializer(serializers.Serializer):
    temp = TempSerializer()
    password = serializers.CharField(max_length=100)


class SignUpEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # regex for email validator
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, attrs['username']):
            user = User.objects.get(email=attrs['username'])
            attrs['username'] = user.username
        # return access and refresh token
        return super().validate(attrs)


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('code', 'name')


class CitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()

    class Meta:
        model = City
        fields = ('code', 'name', 'province')


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('code', 'name', 'city')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('code', 'name', 'skill')


class ProfileSerializer(serializers.ModelSerializer):
    # city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source='city', write_only=True)
    # city =  CitySerializer()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'university', 'city', 'phone_number', 'description')

    # def validate_email(self, value):
    #     if validate_email(value):
    #         raise serializers.ValidationError({'email': _('The address email entered is invalid :))')})
    #     return value
    # TODO this is megabyte ? !!!!
    def validate_avatar_url(self, value):
        MAX_FILE_SIZE = 12000000
        if value.size > MAX_FILE_SIZE:
            raise serializers.ValidationError(
                {'avatar': _('The photo size should be more than %(max_size)d MB.s') % {'max_size': MAX_FILE_SIZE}})
        return value.url


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar_thumbnail',)