from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
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


class InvitationSendView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        sender = self.request.user
        receiver = get_object_or_404(User, id=user_id)

        # Check for existing invitation
        existing_invitation = FriendInvitation.objects.filter(
            sender=sender,
            receiver=receiver,
            status=FriendInvitation.Status.PENDING,
        ).exists()

        if not existing_invitation and sender != receiver:
            FriendInvitation.objects.create(sender=sender, receiver=receiver)

        return HttpResponseRedirect(reverse_lazy('friends-user-search'))


class InvitationAcceptView(LoginRequiredMixin, View):
    pass


class InvitationDeclineView(LoginRequiredMixin, View):
    pass


class InvitationCancelView(LoginRequiredMixin, View):
    pass
