from django.contrib import messages
from django.contrib.auth.forms import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from users.models import Profile
from .forms import (
    ProfileUpdateForm,
    UserUsernameUpdateForm,
    UserEmailUpdateForm,
    UserPasswordUpdateForm,
)


class SettingsView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'users_settings/settings.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('users:settings:general')

    def get_object(self, queryset=None):
        return self.request.user.profile


class SettingsUsernameView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users_settings/username.html'
    form_class = UserUsernameUpdateForm
    success_url = reverse_lazy('users:settings:general')

    def get_form_kwargs(self):
        # Sending user object to the form
        kwargs = super(SettingsUsernameView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        # Update username
        self.object.save(update_fields=['username'])

        messages.success(self.request, 'Username successfully changed!')
        return redirect(self.get_success_url())


class SettingsEmailView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users_settings/email.html'
    form_class = UserEmailUpdateForm
    success_url = reverse_lazy('users:settings:general')

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
    template_name = 'users_settings/password.html'
    form_class = UserPasswordUpdateForm
    success_url = reverse_lazy('users:login')

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
