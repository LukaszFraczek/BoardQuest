from django.urls import path

from .views import FriendsListView, FriendSearchView

urlpatterns = [
    path('<int:pk>/', FriendsListView.as_view(), name='friends-list'),
    path('search/', FriendSearchView.as_view(), name='friends-user-search'),
]
