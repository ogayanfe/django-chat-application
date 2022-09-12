from django.shortcuts import render, redirect
from . import models
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UpdateProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def register_user_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy("home"))
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            models.UserProfile.objects.create(user=user)
            return redirect("home")
        return render(request, template_name="registration/register.html", context={"form": form})

    form = UserCreationForm()
    return render(request=request, template_name="registration/register.html", context={"form": form})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    success_url = reverse_lazy("home")
    model = models.UserProfile
    template_name = "chat/chatroom_edit.html"
    form_class = UpdateProfileForm
    success_url = reverse_lazy("home")

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
