from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from djangorestframework_camel_case.parser import CamelCaseMultiPartParser
from accounts.serializers import *


class ProfileBaseUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class BriefProfileUser(ProfileBaseUser):
    serializer_class = BriefProfileSerializer


class ProfileUser(ProfileBaseUser):
    serializer_class = ProfileSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProfileGetSerializer
        return self.serializer_class


class ProfilePicture(ProfileBaseUser):
    serializer_class = ProfilePictureSerializer
    parser_classes = [CamelCaseMultiPartParser, ]


class ProfileResume(ProfileBaseUser):
    serializer_class = ProfileResumeSerializer
    parser_classes = [CamelCaseMultiPartParser, ]

    def destroy(self, request):
        try:
            self.queryset.filter(id=self.request.user.id).update(resume=None)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserSkill(ProfileBaseUser):
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserSkillSerializer
        elif self.action == 'partial_update':
            return UpdateSkillSerializer
