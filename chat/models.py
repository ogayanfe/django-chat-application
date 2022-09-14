from django.db import models
from django.utils.html import escape
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from django.urls import reverse_lazy


class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    room = models.ForeignKey(
        "ChatRoom", on_delete=models.CASCADE, related_name="messages")

    @property
    def owner_username(self):
        return escape(self.owner.username)

    @property
    def user_profile_picture(self):
        return self.owner.user_profile_info.profile_picture.url

    @property
    def time_created_string(self):
        return f'{naturalday(self.created).title()}, {self.time_created.isoformat("minutes")}'

    def __str__(self):
        return escape(f"{self.owner} | {self.content}")


class ChatRoom(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.CharField(max_length=100, null=False, unique=True)
    members = models.ManyToManyField(User, related_name="chat_rooms")
    created = models.DateTimeField(auto_now_add=True)
    dp = models.ImageField(
        upload_to="images/profile/", blank=True, default="images/profile/groupicon.svg")

    @property
    def last_updated(self):
        if not self.messages.last():
            return ""
        return str(naturaltime(self.messages.last().created))

    @property
    def last_update_time(self):
        if not self.messages.last():
            return ""
        return self.messages.last().created

    @property
    def last_message(self):
        if not self.messages.last():
            return ""
        return escape(f"{self.messages.last().owner.username}: {self.messages.last().content}")

    @property
    def get_absolute_url(self):
        return reverse_lazy("view-conversation", kwargs={"pk": self.id})

    def get_absolute_url(self):
        return reverse_lazy("view-conversation", kwargs={"pk": self.id})

    @property
    def number_of_members(self):
        return self.members.count()

    @property
    def active_members_count(self):
        return self.members.filter(user_profile_info__active=True).count()

    def __str__(self):
        return self.topic
