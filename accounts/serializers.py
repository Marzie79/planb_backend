from rest_framework import serializers
from accounts.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re
from django.core.validators import validate_email
from django.db.models import Q


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
        fields = ('code', 'email',)


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


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('code', 'name', 'province')


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('code', 'name')


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('code', 'name', 'city')   
        
                 
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'city', 'university', 'phone_number', 'description')

    def validate_first_name(self, value):
        if not re.match('^[\u0600-\u06FF\s]+$', value):
            raise serializers.ValidationError({'first_name': ' تنها حروف فارسی مجاز است.'})
        return value

    def validate_last_name(self, value):
        if not re.match('^[\u0600-\u06FF\s]+$', value):
            raise serializers.ValidationError({'last_name': ' تنها حروف فارسی مجاز است.'})
        return value

    def validate_username(self, value):
        if not re.match('^[a-zA-Z0-9]+$', value):
            raise serializers.ValidationError({'username': ' نام کاربری تنها باید شامل حروف و اعداد انگلیسی باشد.'})
        user = User.objects.filter(Q(username=value.lower()))
        if self.instance is not None:
            user = user.exclude(id=self.instance.id)
        if user.exists():
            raise serializers.ValidationError({'username': 'کاربر با این نام کاربری از قبل موجود است.'})
        return value.lower()

    def validate_email(self, value):
        user = self.context['request'].user
        if not validate_email(value):
            raise serializers.ValidationError({'email': 'آدرس ایمیل وارد شده نامعتبر است.'})
        elif User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({'email': 'کابر با این آدرس ایمیل از قبل موجود است.'})
        return value

    def validate_phone_number(self, value):
        if value.startswith('0'):
            value = value[1:]
            user = User.objects.filter(Q(phone_number=value))
            if self.instance is not None:
                user = user.exclude(id=self.instance.id)
            if user.exists():
                raise serializers.ValidationError({'phone_number': 'کاربر با این تلفن همراه از قبل موجود است.'})
        return value

    def validate_avatar_url(self, value):
        MAX_FILE_SIZE = 12000000
        if value.size > MAX_FILE_SIZE:
            raise serializers.ValidationError({'avatar': 'حجم عکس نباید بیشتر از {} مگابایت باشد.'.format(MAX_FILE_SIZE)})
        return value.url
