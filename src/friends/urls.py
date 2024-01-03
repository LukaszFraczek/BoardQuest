from django.urls import path

from .views import (
    FriendsListView,
    FriendSearchView,
    FriendRemoveView,
    InvitesSentListView,
    InvitesReceivedListView,
    InvitationCreateView,
    InvitationAcceptView,
    InvitationDeclineView,
    InvitationCancelView,
)

urlpatterns = [
    path('<int:user_id>/', FriendsListView.as_view(), name='friends-list'),
    path('search/', FriendSearchView.as_view(), name='friends-user-search'),
    path('invites-received/', InvitesReceivedListView.as_view(), name='friends-invites-received'),
    path('invites-sent/', InvitesSentListView.as_view(), name='friends-invites-sent'),
    path('invitation-create/<int:user_id>/', InvitationCreateView.as_view(), name='friends-invitation-create'),
    path('invitation-accept/<int:user_id>/', InvitationAcceptView.as_view(), name='friends-invitation-accept'),
    path('invitation-decline/<int:user_id>/', InvitationDeclineView.as_view(), name='friends-invitation-decline'),
    path('invitation-cancel/<int:user_id>/', InvitationCancelView.as_view(), name='friends-invitation-cancel'),
    path('remove/<int:user_id>/', FriendRemoveView.as_view(), name='friends-remove-friend'),
]
