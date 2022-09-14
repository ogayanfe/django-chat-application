from django import forms
from accounts.models import UserProfile
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from django.template.defaultfilters import filesizeformat
from django.contrib.auth.models import User


class UpdateProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("profile_picture",)

    def clean_profile_picture(self):
        file = self.cleaned_data.get("profile_picture")
        max_size = settings.MAX_IMAGE_SIZE  # 256.0kb
        error = f'File is to large, max_size is {filesizeformat(max_size)}. Current Size is {filesizeformat(file.size)}'
        if file.size > max_size:
            raise forms.ValidationError(error)
        return file


class UpdateUserInfoForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "password")
