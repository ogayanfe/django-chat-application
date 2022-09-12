from django.urls import path, re_path
from . import views
from django.contrib.auth import views as authviews

urlpatterns = [
    path("signup/", views.register_user_view, name="signup"),
    path("profile-image/<int:pk>/update/",
         views.UpdateProfileView.as_view(), name="profile_update"),
    path("login/", authviews.LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("logout/", authviews.LogoutView.as_view(), name="logout")

]
