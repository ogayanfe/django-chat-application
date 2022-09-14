from django.urls import path, include
from .views import HomeView, ChatDetailView, ChatRoomCreateView, ChatRoomUpdateView, ChatRoomDeleteView

urlpatterns = (
    path("", HomeView.as_view(), name="home"),
    path("chat/<int:pk>/", ChatDetailView.as_view(), name="view-conversation"),
    path("chat/api/", include("chat.api.urls")),
    path("chatroom/create", ChatRoomCreateView.as_view(), name="create-room"),
    path("chatroom/<int:pk>/edit", ChatRoomUpdateView.as_view(), name="update-room"),
    path("chatroom/<int:pk>/delete",
         ChatRoomDeleteView.as_view(), name="delete-room"),
)
