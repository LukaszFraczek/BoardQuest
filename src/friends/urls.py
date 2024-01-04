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


app_name = 'friends'
urlpatterns = [
    path(f'{PREFIX}/<int:user_id>/', FriendsListView.as_view(), name='list'),
    path(f'{PREFIX}/search/', FriendSearchView.as_view(), name='user-search'),
    path(f'{PREFIX}/invitations/received/', InvitesReceivedListView.as_view(), name='invites-received'),#  'friends:invites-received'
    path(f'{PREFIX}/invitations/sent/', InvitesSentListView.as_view(), name='invites-sent'),
    path(f'{PREFIX}/invitations/<int:user_id>/create/', InvitationCreateView.as_view(), name='invitation-create'),
    path(f'{PREFIX}/invitations/<int:user_id>/accept', InvitationAcceptView.as_view(), name='invitation-accept'),
    path(f'{PREFIX}/invitations/<int:user_id>/decline/', InvitationDeclineView.as_view(), name='invitation-decline'),
    path(f'{PREFIX}/invitations/<int:user_id>/cancel/', InvitationCancelView.as_view(), name='invitation-cancel'),
    path(f'{PREFIX}/remove/<int:user_id>/', FriendRemoveView.as_view(), name='remove-friend'),
]
