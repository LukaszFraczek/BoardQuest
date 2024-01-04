from django.urls import path, include

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

NAMESPACE = 'friends'
NAMESPACE_INVITATIONS = 'invitations'
URL_PREFIX = 'friends/'
URL_PREFIX_INVITATIONS = 'invitations/'


friends_invitations_patterns = [
    path('sent/', InvitesSentListView.as_view(), name='sent'),
    path('received/', InvitesReceivedListView.as_view(), name='received'),
    path('<int:user_id>/create/', InvitationCreateView.as_view(), name='create'),
    path('<int:user_id>/accept', InvitationAcceptView.as_view(), name='accept'),
    path('<int:user_id>/decline/', InvitationDeclineView.as_view(), name='decline'),
    path('<int:user_id>/cancel/', InvitationCancelView.as_view(), name='cancel'),
]

namespace_patterns_invitations = (friends_invitations_patterns, NAMESPACE_INVITATIONS)

friends_patterns = [
    path('<int:user_id>/', FriendsListView.as_view(), name='list'),
    path('search/', FriendSearchView.as_view(), name='search'),
    path('remove/<int:user_id>/', FriendRemoveView.as_view(), name='remove-friend'),
    path(f'{URL_PREFIX_INVITATIONS}', include(namespace_patterns_invitations))
]

namespace_patterns = (friends_patterns, NAMESPACE)

urlpatterns = [
    path(f'{URL_PREFIX}', include(namespace_patterns)),
]
