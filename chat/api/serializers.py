from xmlrpc.client import Boolean
from django.utils.html import escape
from chat.models import ChatRoom, Message
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("username", "profile_image", "active")

    def get_profile_image(self, obj):
        return str(obj.user_profile_info.profile_picture.url)

    def get_username(self, obj):
        return escape(obj.username)

    def get_active(self, obj):
        return Boolean(obj.user_profile_info.active)


class MessageSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "content",
            "owner_username",
            "is_owner",
            "user_profile_picture",
            "time_created_string"
        )

    def get_content(self, obj):
        return escape(obj.content)

    def get_is_owner(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return user == obj.owner


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = (
            "topic",
            "last_message",
            "last_updated",
            "get_absolute_url",
            "dp"
        )


class ChatRoomWithMessagesSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    members = UserSerializer(many=True)
    topic = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = (
            "topic",
            "last_message",
            "last_updated",
            "members",
            "messages",
            "number_of_members",
            "active_members_count",
            "dp"
        )

    def topic(self, obj):
        return escape(obj.topic)
