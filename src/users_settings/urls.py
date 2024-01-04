from django.urls import path, include

from .views import (
    SettingsView,
    SettingsUsernameView,
    SettingsEmailView,
    SettingsPasswordView,
)

PREFIX = 'users/settings/'

urlpatterns = [
    path(f'{PREFIX}/', SettingsView.as_view(), name='user-settings'),
    path(f'{PREFIX}/username/', SettingsUsernameView.as_view(), name='settings-username'),
    path(f'{PREFIX}/email/', SettingsEmailView.as_view(), name='settings-email'),
    path(f'{PREFIX}/password/', SettingsPasswordView.as_view(), name='settings-password'),
]
