from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.models import Reciever, Message
from core.pagination import Pagination
from dashboard.serializers.serializer_message import MessageSerializer


class MessageView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    pagination_class = Pagination

    def get_queryset(self):
        return Message.objects.filter(reciever__user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        recievers = Reciever.objects.filter(message__in=page).filter(user=request.user)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            recievers.update(is_visited=True)
            return result
        serializer = self.get_serializer(queryset, many=True)
        recievers.update(is_visited=True)
        return Response(serializer.data)
