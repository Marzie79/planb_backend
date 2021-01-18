from rest_framework import serializers
from accounts.models import *
from .serializer_profile import *

class UserInfoSerializer(serializers.ModelSerializer):
    from .serializer_list import UniversitySerializer
    phone_number = serializers.SerializerMethodField('check_phone_number_visiblity')
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    city = CityProfileSerializer()
    university = UniversitySerializer()
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','university','gender_display','phone_number','city','resume', 'avatar')
        extra_kwargs = {
            'url': {'lookup_field':'username','read_only':'True','view_name':'user-detail'}
        }

    def check_phone_number_visiblity(self, instance):
        if instance.username == self.context['request'].user.username:
            return 1
            # return User.objects.get(username=instance.username).phone_number
        else:
            return None    

# class GetUserInfoSerializer(UserInfoSerializer):
#     from .serializer_list import UniversitySerializer
#     gender_display = serializers.CharField(source='get_gender_display', read_only=True)
#     city = CityProfileSerializer()
#     university = UniversitySerializer()

#     class Meta:
#         model = User
#         fields = UserInfoSerializer.Meta.fields + ('gender_display',)