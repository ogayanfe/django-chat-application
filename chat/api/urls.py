from django.urls import path
import chat.api.views as chat_api_views

urlpatterns = (
    path("all_rooms/", chat_api_views.GroupListAPIView.as_view()),
    path("room/<int:pk>/", chat_api_views.GroupRetriveAPIView.as_view())
)
