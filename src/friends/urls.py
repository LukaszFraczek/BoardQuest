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
    path('invitation-accept/<int:user_id>/', InvitationAcceptView.as_view(), name='friends-invitation-accept'),
    path('invitation-decline/<int:user_id>/', InvitationDeclineView.as_view(), name='friends-invitation-decline'),
    path('invitation-cancel/<int:user_id>/', InvitationCancelView.as_view(), name='friends-invitation-cancel'),
]
