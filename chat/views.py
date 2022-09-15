from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ChatRoom
from django.urls import reverse_lazy
from .forms import ChatRoomCreateForm
from accounts.mixins import CreateUserProfileInstanceIfUserIsAuthenticated


class HomeView(CreateUserProfileInstanceIfUserIsAuthenticated, ListView):
    template_name = "chat/index.html"
    paginate_by = 10
    model = ChatRoom

    def get_queryset(self):
        qs = super().get_queryset()
        searchText = self.request.GET.get("search", "").lower()
        qs = qs.filter(topic__icontains=searchText)
        filter = self.request.GET.get("filter", "")
        if self.request.user.is_authenticated and filter == "":
            qs = qs.filter(members__id=self.request.user.id)
        result = list(
            sorted(
                qs, key=lambda room: room.created if not room.messages.last(
                ) else room.messages.last().created
            )
        )
        return result[::-1]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active"] = self.request.GET.get("filter", "inbox")
        return context


class ChatDetailView(LoginRequiredMixin, CreateUserProfileInstanceIfUserIsAuthenticated, DetailView):
    model = ChatRoom
    template_name = "chat/chat.html"


class ChatRoomCreateView(LoginRequiredMixin, CreateUserProfileInstanceIfUserIsAuthenticated, CreateView):
    model = ChatRoom
    template_name = "chat/chatroom_edit.html"
    form_class = ChatRoomCreateForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        object = form.save(commit=False)
        object.creator = self.request.user
        object.save()
        object.members.add(self.request.user)
        return super().form_valid(form)


class ChatRoomUpdateView(LoginRequiredMixin, CreateUserProfileInstanceIfUserIsAuthenticated, UpdateView):
    model = ChatRoom
    template_name = "chat/chatroom_edit.html"
    form_class = ChatRoomCreateForm
    success_url = reverse_lazy("home")

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(creator=self.request.user)


class ChatRoomDeleteView(LoginRequiredMixin, DeleteView):
    model = ChatRoom
    success_url = reverse_lazy("home")
    template_name = "chat/delete.html"

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)
