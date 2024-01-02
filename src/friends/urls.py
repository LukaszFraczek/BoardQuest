from django.urls import path

from .views import (
    FriendsListView,
    FriendSearchView,
    InvitationSendView,
    InvitationAcceptView,
    InvitationDeclineView,
    InvitationCancelView,
)

urlpatterns = [
    path('<int:user_id>/', FriendsListView.as_view(), name='friends-list'),
    path('search/', FriendSearchView.as_view(), name='friends-user-search'),
    path('invitation-send/<int:user_id>/', InvitationSendView.as_view(), name='friends-invitation-send'),
    path('invitation-accept/', InvitationAcceptView.as_view(), name='friends-invitation-accept'),
    path('invitation-decline/', InvitationDeclineView.as_view(), name='friends-invitation-decline'),
    path('invitation-cancel/', InvitationCancelView.as_view(), name='friends-invitation-cancel'),
]
