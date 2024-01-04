from django.urls import path, include

from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    ProfileView,
)

NAMESPACE = 'users'
URL_PREFIX = 'users/'


patterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
]

all_patterns = [
    path(f'{URL_PREFIX}', include(patterns)),
    path('', include('users_settings.urls')),
]

namespace_patterns = (all_patterns, NAMESPACE)

urlpatterns = [
    path('', include(namespace_patterns)),
]
