from django.urls import path

from .views import FriendsListView

urlpatterns = [
    path('<int:pk>/', FriendsListView.as_view(), name='friends-list'),
]
