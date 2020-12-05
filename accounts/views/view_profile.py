from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from djangorestframework_camel_case.parser import CamelCaseMultiPartParser

from accounts.serializers import *


class ProfileUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        """
            Returns the object the view is displaying.
        """
        return self.request.user

# def get_redirected(queryset_or_class, lookups, validators):
#     obj = get_object_or_404(queryset_or_class, **lookups)
#     for key, value in validators.items():
#         if value != getattr(obj, key):
#             return obj
#     return obj


class ProfilePicture(ProfileUser):
    serializer_class = ProfilePictureSerializer
    parser_classes = [CamelCaseMultiPartParser,]

    def post(self, request):
        return Response({'received data': request.data})