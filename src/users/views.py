from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .models import Profile
from friends.models import FriendList
from .forms import (
    UserLoginForm,
    UserRegisterForm,
    ProfileUpdateForm,
    UserUsernameUpdateForm,
    UserEmailUpdateForm,
    UserPasswordUpdateForm,
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
        # logic for a failed login
        messages.warning(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    pass


class ProfileView(LoginRequiredMixin, TemplateView):
    model = Profile
    template_name = 'users/profile.html'


class SettingsView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'users/settings.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('user-settings')

    def get_object(self, queryset=None):
        return self.request.user.profile


class SettingsUsernameView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/settings/username.html'
    form_class = UserUsernameUpdateForm
    success_url = reverse_lazy('user-settings')

    def get_form_kwargs(self):
        # Sending user object to the form
        kwargs = super(SettingsUsernameView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        # Get data from the form
        new_username = form.cleaned_data.get('username')
        new_username_conf = form.cleaned_data.get('username_confirm')
        password_conf = form.cleaned_data.get('password_confirm')

        # # Check if entered password is correct
        # if not check_password(password_conf, self.request.user.password):
        #     form.add_error('password_confirm', 'Incorrect password. Please try again.')
        #     return self.form_invalid(form)

        # # Check if entered usernames are the same
        # if new_username != new_username_conf:
        #     form.add_error('username', 'Usernames do not match each other.')
        #     return self.form_invalid(form)

        # # Check if entered username is unique
        # if User.objects.filter(username=new_username).exclude(pk=self.request.user.pk).exists():
        #     form.add_error('username', 'Username taken. Please choose a different one.')
        #     return self.form_invalid(form)
        #
        # # Check if entered username is users' current username
        # if new_username == self.request.user.username:
        #     form.add_error('username', 'Username taken. Please choose a different one.')
        #     return self.form_invalid(form)

        # Update username
        self.object.save(update_fields=['username'])

        messages.success(self.request, 'Username successfully changed!')
        return redirect(self.get_success_url())


class SettingsEmailView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/settings/email.html'
    form_class = UserEmailUpdateForm
    success_url = reverse_lazy('user-settings')

    def get_form_kwargs(self):
        # Sending user object to the form
        kwargs = super(SettingsEmailView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        # Update email
        self.object.save(update_fields=['email'])

        messages.success(self.request, 'Email successfully changed!')
        return redirect(self.get_success_url())


class SettingsPasswordView(LoginRequiredMixin, PasswordChangeView):
    model = User
    template_name = 'users/settings/password.html'
    form_class = UserPasswordUpdateForm
    success_url = reverse_lazy('user-login')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        # Sending user object to the form
        kwargs = super(SettingsPasswordView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Password successfully changed!')
        return super().form_valid(form)
