from django.db import models
from django.contrib.auth.models import User
import hashlib


def user_directory_path(instance, filename):
    extension = filename.split(".").pop()
    directory_name = f"{instance.user.username}_{instance.user.id}"
    hash = hashlib.md5(str(instance.user.id).encode()).hexdigest()
    return f"images/profile/{directory_name}/{hash}.{extension}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name="user_profile_info", on_delete=models.CASCADE
    )
    active = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to=user_directory_path, default="images/profile/defaultprofile.svg")

    def __str__(self):
        return str(self.user.username.title()) + " Profile Data"
