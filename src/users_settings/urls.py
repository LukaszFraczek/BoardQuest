from django.urls import path, include

from .views import (
    SettingsView,
    SettingsUsernameView,
    SettingsEmailView,
    SettingsPasswordView,
)

NAMESPACE = 'settings'
PREFIX = 'users/settings/'

patterns = [
    path('', SettingsView.as_view(), name='general'),
    path('username/', SettingsUsernameView.as_view(), name='username'),
    path('email/', SettingsEmailView.as_view(), name='email'),
    path('password/', SettingsPasswordView.as_view(), name='password'),
]

users_settings_patterns = (patterns, NAMESPACE)

urlpatterns = [
    path(f'{PREFIX}', include(users_settings_patterns)),
]
