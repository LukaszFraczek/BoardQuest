from django.urls import path

from .views import UserRegisterView, UserLoginView, UserLogoutView, ProfileView, SettingsView, ChangeUsernameView
from src import settings


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('settings/', SettingsView.as_view(), name='user-settings'),
]
