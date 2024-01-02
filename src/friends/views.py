from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView

from users.models import Profile
from .models import FriendList, FriendInvitation


class FriendsListView(LoginRequiredMixin, ListView):
    template_name = 'friends/friendlist.html'
    context_object_name = 'friends'

    def get_queryset(self):
        friend_list = get_object_or_404(FriendList, user=self.kwargs['pk'])
        friends = friend_list.friends.all()
        return Profile.objects.filter(user__in=friends)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_list'] = get_object_or_404(FriendList, user=self.kwargs['pk'])
        return context


class FriendSearchView(LoginRequiredMixin, ListView):
    template_name = 'friends/search.html'
    context_object_name = 'search_result'

    def get_queryset(self):
        queryset = User.objects.all()

        # Search for specified username in querystring
        username = self.request.GET.get('username')
        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset


class FriendInvitesView(LoginRequiredMixin):
    pass

