from socket import fromshare
from django import forms
from chat.models import ChatRoom
from django.core.exceptions import ValidationError


class ChatRoomCreateForm(forms.ModelForm):
    topic = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = ChatRoom
        fields = ("topic",)
