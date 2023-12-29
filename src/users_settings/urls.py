from django.urls import path, include

from .views import (
    SettingsView,
    SettingsUsernameView,
    SettingsEmailView,
    SettingsPasswordView,
)


urlpatterns = [
    path('', SettingsView.as_view(), name='user-settings'),
    path('username/', SettingsUsernameView.as_view(), name='settings-username'),
    path('email/', SettingsEmailView.as_view(), name='settings-email'),
    path('password/', SettingsPasswordView.as_view(), name='settings-password'),
]
