from rest_framework import serializers

from accounts.models import NotificationToken


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationToken
        fields = ('token', 'device', 'browser', 'user')
