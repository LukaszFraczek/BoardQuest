from django.urls import path, include

from .views import (
    FriendsListView,
    FriendSearchView,
    FriendRemoveView,
    InvitationsSentListView,
    InvitationsReceivedListView,
    InvitationsCreateView,
    InvitationsAcceptView,
    InvitationsDeclineView,
    InvitationsCancelView,
)

NAMESPACE = 'friends'
NAMESPACE_INVITATIONS = 'invitations'
URL_PREFIX = 'friends/'
URL_PREFIX_INVITATIONS = 'invitations/'


friends_invitations_patterns = [
    path('sent/', InvitationsSentListView.as_view(), name='sent'),
    path('received/', InvitationsReceivedListView.as_view(), name='received'),
    path('create/', InvitationsCreateView.as_view(), name='create'),
    path('accept', InvitationsAcceptView.as_view(), name='accept'),
    path('decline/', InvitationsDeclineView.as_view(), name='decline'),
    path('cancel/', InvitationsCancelView.as_view(), name='cancel'),
]

namespace_patterns_invitations = (friends_invitations_patterns, NAMESPACE_INVITATIONS)

friends_patterns = [
    path('<int:user_id>/', FriendsListView.as_view(), name='list'),
    path('search/', FriendSearchView.as_view(), name='search'),
    path('remove/', FriendRemoveView.as_view(), name='remove-friend'),
    path(f'{URL_PREFIX_INVITATIONS}', include(namespace_patterns_invitations))
]

namespace_patterns = (friends_patterns, NAMESPACE)

urlpatterns = [
    path(f'{URL_PREFIX}', include(namespace_patterns)),
]
