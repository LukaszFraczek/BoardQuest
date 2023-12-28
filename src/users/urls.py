from django.urls import path

from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    ProfileView,
    SettingsView,
    SettingsUsernameView,
    SettingsEmailView,
    SettingsPasswordView,
)


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='user-profile'),
    path('settings/', SettingsView.as_view(), name='user-settings'),
    path('settings/username/', SettingsUsernameView.as_view(), name='settings-username'),
    path('settings/email/', SettingsEmailView.as_view(), name='settings-email'),
    path('settings/password/', SettingsPasswordView.as_view(), name='settings-password'),
]
