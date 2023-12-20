from django.urls import path

from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    ProfileView,
    SettingsView,
    ChangeUsernameView,
    ChangeEmailView,
)


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('settings/', SettingsView.as_view(), name='user-settings'),
    path('settings/username/', ChangeUsernameView.as_view(), name='settings-username'),
    path('settings/email/', ChangeEmailView.as_view(), name='settings-email'),
    path('settings/password/', SettingsView.as_view(), name='settings-password'),
]
