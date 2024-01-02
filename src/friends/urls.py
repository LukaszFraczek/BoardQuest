from django.urls import path

from .views import FriendsListView, FriendSearchView

urlpatterns = [
    path('<int:user_id>/', FriendsListView.as_view(), name='friends-list'),
    path('search/', FriendSearchView.as_view(), name='friends-user-search'),
]
