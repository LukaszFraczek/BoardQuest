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

PREFIX = 'friends'

urlpatterns = [
    path(f'{PREFIX}/<int:user_id>/', FriendsListView.as_view(), name='friends-list'),
    path(f'{PREFIX}/search/', FriendSearchView.as_view(), name='friends-user-search'),
    path(f'{PREFIX}/invitations/received/', InvitesReceivedListView.as_view(), name='friends-invites-received'),#  'friends:invites-received'
    path(f'{PREFIX}/invitations/sent/', InvitesSentListView.as_view(), name='friends-invites-sent'),
    path(f'{PREFIX}/invitations/<int:user_id>/create/', InvitationCreateView.as_view(), name='friends-invitation-create'),
    path(f'{PREFIX}/invitations/<int:user_id>/accept', InvitationAcceptView.as_view(), name='friends-invitation-accept'),
    path(f'{PREFIX}/invitations/<int:user_id>/decline/', InvitationDeclineView.as_view(), name='friends-invitation-decline'),
    path(f'{PREFIX}/invitations/<int:user_id>/cancel/', InvitationCancelView.as_view(), name='friends-invitation-cancel'),
    path(f'{PREFIX}/remove/<int:user_id>/', FriendRemoveView.as_view(), name='friends-remove-friend'),
]
