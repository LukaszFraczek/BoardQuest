from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView

from users.models import Profile
from .models import FriendList, FriendInvitation


class FriendsListView(LoginRequiredMixin, ListView):
    template_name = 'friends/friendlist.html'
    context_object_name = 'users'

    def get_queryset(self):
        friend_list = get_object_or_404(FriendList, user=self.kwargs['user_id'])
        friends = friend_list.friends.all()
        return User.objects.filter(id__in=friends)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_list'] = get_object_or_404(FriendList, user=self.kwargs['user_id'])
        return context


class FriendSearchView(LoginRequiredMixin, ListView):
    template_name = 'friends/search.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = None

        # Search for specified username in querystring
        username = self.request.GET.get('username')
        if username:
            queryset = User.objects.filter(username__icontains=username)

        return queryset


class FriendInvitesView(LoginRequiredMixin):
    pass

