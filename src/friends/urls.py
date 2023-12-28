from django.urls import path

from .views import FriendsListView

urlpatterns = [
    path('list/', FriendsListView.as_view(), name='friends-list'),
]
