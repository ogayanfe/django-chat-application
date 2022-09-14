from django.urls import path
from . import views
from django.contrib.auth import views as authviews

urlpatterns = [
    path("signup/", views.register_user_view, name="signup"),
    path("profile-image/<int:pk>/update/",
         views.UpdateProfilePictureView.as_view(), name="profile-image-update"),
    path("login/", authviews.LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("logout/", authviews.LogoutView.as_view(), name="logout"),
    path("update/password/",
         authviews.PasswordChangeView.as_view(template_name="registration/form.html", success_url="/"), name="password-change"),
    path("update/<int:pk>/", views.UpdateUserInfoView.as_view(),
         name="profile-update"),
]
