from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from friends.models import FriendList
from .models import Profile
from .forms import (
    UserLoginForm,
    UserRegisterForm,
)


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('user-login')
    success_message = "Welcome, %(username)s. You have successfully signed up!"


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('homepage')

    def form_invalid(self, form):
        messages.warning(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    pass


class ProfileView(DetailView):
    template_name = 'users/profile.html'
    model = Profile

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.kwargs['user_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_list = get_object_or_404(FriendList, user=self.kwargs['user_id'])
        friend_ids = friend_list.friends.all()
        context['friends'] = User.objects.filter(id__in=friend_ids).order_by('id')[:3]  # TODO: add a system to decide which 3 firends are shown
        return context
