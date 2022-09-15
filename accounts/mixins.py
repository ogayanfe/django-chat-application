from .models import UserProfile


class CreateUserProfileInstanceIfUserIsAuthenticated:
    # The function of this code is to ensure that every user gets and authmatically generated
    # user profile
    def get(self, *args):
        user = self.request.user if self.request.user.is_authenticated else None
        if not UserProfile.objects.filter(user=user).exists():
            UserProfile.objects.create(user=user)
        return super().get(*args)
