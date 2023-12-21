from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import FriendList, FriendInvitation


class FriendsListView(LoginRequiredMixin, ListView):
    model = FriendList
    template_name = 'friends/friendlist.html'
    context_object_name = 'friends'


class FriendInvitesView(LoginRequiredMixin):
    pass


class FriendSearchView(LoginRequiredMixin):
    pass
