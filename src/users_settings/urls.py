from django.urls import path, include

from .views import (
    SettingsView,
    SettingsUsernameView,
    SettingsEmailView,
    SettingsPasswordView,
)

NAMESPACE = 'settings'
URL_PREFIX = 'users/settings/'

patterns = [
    path('', SettingsView.as_view(), name='general'),
    path('username/', SettingsUsernameView.as_view(), name='username'),
    path('email/', SettingsEmailView.as_view(), name='email'),
    path('password/', SettingsPasswordView.as_view(), name='password'),
]

namespace_patterns = (patterns, NAMESPACE)

urlpatterns = [
    path(f'{URL_PREFIX}', include(namespace_patterns)),
]
