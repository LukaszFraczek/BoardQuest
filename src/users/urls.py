from django.urls import path, include

from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    ProfileView,
)

PREFIX = 'users'

urlpatterns = [
    path(f'{PREFIX}/register/', UserRegisterView.as_view(), name='user-register'),
    path(f'{PREFIX}/login/', UserLoginView.as_view(), name='user-login'),
    path(f'{PREFIX}/logout/', UserLogoutView.as_view(), name='user-logout'),
    path(f'{PREFIX}/profile/<int:user_id>/', ProfileView.as_view(), name='user-profile'),
    path('', include('users_settings.urls')),
]
