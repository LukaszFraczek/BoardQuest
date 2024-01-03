from django.urls import path, include

from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    ProfileView,
)


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='user-profile'),
    path('settings/', include('users_settings.urls')),
]
