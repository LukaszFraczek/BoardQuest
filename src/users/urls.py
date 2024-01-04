from django.urls import path, include

from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    ProfileView,
)

PREFIX = 'users'


app_name = 'users'
urlpatterns = [
    path(f'{PREFIX}/register/', UserRegisterView.as_view(), name='register'),
    path(f'{PREFIX}/login/', UserLoginView.as_view(), name='login'),
    path(f'{PREFIX}/logout/', UserLogoutView.as_view(), name='logout'),
    path(f'{PREFIX}/profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('', include('users_settings.urls')),
]
