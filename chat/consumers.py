import json
import chat.models as chatmodels
import accounts.models as accountmodels
from django.forms.models import model_to_dict
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.html import escape

MAX_MESSAGE_COUNT = 20


class ChatConsumer(AsyncWebsocketConsumer):
    room_name = None
    room_group_name = None
    user = None
    id = None

    async def connect(self):
        self.id = self.scope["url_route"]["kwargs"]["id"]
        self.room_name = await self.get_room_name(self.id)
        self.room_group_name = f"chat_{self.id}"
        self.user = self.scope["user"]
        if not (self.user):
            return
        await self.accept()
        await self.add_to_room(self.user)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.update_active_status(True)

    async def receive(self, text_data=None, bytes_data=None):
        if not (text_data or bytes_data):
            return
        message = json.loads(text_data)
        message_content = message["message"]
        response_message = await self.save_message_to_chatroom(message_content=message_content)
        response_message["active_count"] = await self.active_count()
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "send_message",
                "message": response_message,
            }
        )

    async def send_message(self, event):
        await self.send(json.dumps(event["message"]))

    async def disconnect(self, *args, **kwargs):
        await self.update_active_status(False)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def add_to_room(self, user):
        room = chatmodels.ChatRoom.objects.all().get(topic=self.room_name)
        if not room:
            return False
        room.members.add(user)
        return True

    @database_sync_to_async
    def save_message_to_chatroom(self, message_content):
        room = chatmodels.ChatRoom.objects.all().get(topic=self.room_name)
        if (room.messages.count() == MAX_MESSAGE_COUNT):
            room.messages.first().delete()
        message = room.messages.create(
            owner=self.user, content=message_content)
        response = model_to_dict(message)
        response["profile_picture"] = self.user.user_profile_info.profile_picture.url
        response["username"] = escape(message.owner.username)
        response["content"] = escape(response.get("content"))
        response["created_date"] = message.time_created_string
        return response

    @database_sync_to_async
    def update_active_status(self, active):
        # Add user to room if he's not already a member
        info, created = accountmodels.UserProfile.objects.get_or_create(
            user=self.user
        )
        info.active = active
        info.save()

    @database_sync_to_async
    def active_count(self):
        room = chatmodels.ChatRoom.objects.get(topic=self.room_name)
        return str(room.active_members_count)

    @database_sync_to_async
    def get_room_name(self, id):
        return chatmodels.ChatRoom.objects.get(pk=id).topic
