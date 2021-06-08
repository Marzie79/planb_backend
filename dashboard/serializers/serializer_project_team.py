from rest_framework import serializers

from accounts.models import UserProject
from core.fields import CustomHyperlinkedRelatedField


class ProjectTeamSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='user.avatar', required=False, )
    city = serializers.ReadOnlyField(source='user.city.name')
    description = serializers.ReadOnlyField(source='user.description')
    name = serializers.ReadOnlyField(source='user.__str__')
    province = serializers.ReadOnlyField(source='user.city.province.name')
    role = serializers.ReadOnlyField(source='get_role_display')
    username = serializers.ReadOnlyField(source='user.username')
    url = CustomHyperlinkedRelatedField(
        **{'source': 'user', 'lookup_field': 'username', 'read_only': 'True', 'view_name': 'user-detail'})

    class Meta:
        model = UserProject
        fields = (
            'name', 'city', 'role', 'province', 'description', 'avatar', 'status', 'username', 'user', 'project', 'url')
        # extra_kwargs = {
        #     'status': {'write_only': True},
        # }


# class PersonSerializer(serializers.ModelSerializer):
#     city = serializers.ReadOnlyField(source='city.name')
#     name = serializers.ReadOnlyField(source='__str__')
#     province = serializers.ReadOnlyField(source='city.province.name')
#     role = serializers.ReadOnlyField(source='get_role_display')
#
#     class Meta:
#         model = User
#         fields = ('name', 'city', 'role', 'province', 'description', 'avatar', 'username')
