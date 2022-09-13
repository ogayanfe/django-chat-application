from rest_framework.generics import ListAPIView, RetrieveAPIView
from chat import models as chat_models
import chat.api.serializers as chatserializers


class GroupListAPIView(ListAPIView):
    queryset = chat_models.ChatRoom.objects.all()
    serializer_class = chatserializers.ChatRoomSerializer

    def get_queryset(self):
        qs = super().get_queryset().filter(members__id=self.request.user.id)
        result = list(
            sorted(
                qs, key=lambda room: room.created if not room.messages.last(
                ) else room.messages.last().created
            )
        )
        return result[::-1]


class GroupRetriveAPIView(RetrieveAPIView):
    serializer_class = chatserializers.ChatRoomWithMessagesSerializer
    queryset = chat_models.ChatRoom.objects.all()
