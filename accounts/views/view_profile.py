from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from djangorestframework_camel_case.parser import CamelCaseMultiPartParser
from accounts.serializers import *


class ProfileUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class ProfilePicture(ProfileUser):
    serializer_class = ProfilePictureSerializer
    parser_classes = [CamelCaseMultiPartParser,]


class ProfileResume(ProfileUser):
    serializer_class = ProfileResumeSerializer
    parser_classes = [CamelCaseMultiPartParser,]


class UserSkill(ProfileUser):

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserSkillSerializer
        elif self.action == 'partial_update':
            return UpdateSkillSerializer