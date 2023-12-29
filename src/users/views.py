from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .models import Profile
from friends.models import FriendList
from .forms import (
    UserLoginForm,
    UserRegisterForm,
)


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('user-login')
    success_message = "Welcome, %(username)s. You have successfully signed up!"

    def form_valid(self, form):
        response = super().form_valid(form)

        # Create a profile & friend list for new user
        Profile.objects.create(user=self.object)
        FriendList.objects.create(user=self.object)

        return response


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
    model = Profile
    template_name = 'users/profile.html'
