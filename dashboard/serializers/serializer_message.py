from rest_framework import serializers

from accounts.models import Message, Reciever, NotificationToken


class MessageSerializer(serializers.ModelSerializer):
    is_visited = serializers.SerializerMethodField('is_visited_value')

    class Meta:
        model = Message
        fields = ["is_visited", "text", "id", "created_date"]

    def is_visited_value(self, instance):
        user = self.context['request'].user
        return Reciever.objects.get(user=user, message=instance).is_visited


