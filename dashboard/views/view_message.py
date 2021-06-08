from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.models import Reciever, Message
from core.pagination import Pagination
from dashboard.serializers.serializer_message import MessageSerializer


class MessageView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    pagination_class = Pagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Message.objects.filter(reciever__user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        recievers = Reciever.objects.filter(message__in=page).filter(user=request.user)
        recievers.update(is_visited=True)
       # if len(page):
        serializer = self.get_serializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        return result
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
