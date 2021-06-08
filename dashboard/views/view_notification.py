from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from accounts.models import NotificationToken
from dashboard.serializers.serializer_notification import NotificationSerializer


class NotificationView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = NotificationToken.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return NotificationToken.objects.filter(user=self.request.user)