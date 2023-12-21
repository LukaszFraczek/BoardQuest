from django.urls import path

from .views import FriendsListView

urlpatterns = [
    path('register/', FriendsListView.as_view(), name='friends-list'),
]
