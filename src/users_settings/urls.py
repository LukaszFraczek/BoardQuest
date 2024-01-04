from django.urls import path, include

from .views import (
    SettingsView,
    SettingsUsernameView,
    SettingsEmailView,
    SettingsPasswordView,
)

PREFIX = 'users/settings'


app_name = 'users_settings'
urlpatterns = [
    path(f'{PREFIX}/', SettingsView.as_view(), name='general'),
    path(f'{PREFIX}/username/', SettingsUsernameView.as_view(), name='username'),
    path(f'{PREFIX}/email/', SettingsEmailView.as_view(), name='email'),
    path(f'{PREFIX}/password/', SettingsPasswordView.as_view(), name='password'),
]
