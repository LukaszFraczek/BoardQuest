from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import FriendList, FriendInvitation


class FriendsListView(LoginRequiredMixin, ListView):
    template_name = 'friends/friend_list.html'
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


class FriendRemoveView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        current_user = self.request.user
        selected_user = get_object_or_404(User, id=user_id)

        current_user.friendlist.end_friendship(selected_user)

        return HttpResponseRedirect(reverse_lazy('friends:list'))


class InvitesSentListView(LoginRequiredMixin, ListView):
    template_name = 'friends/invites_sent.html'
    context_object_name = 'users'

    def get_queryset(self):
        invitation_receiver_ids = FriendInvitation.objects.filter(
            sender=self.request.user,
            status=FriendInvitation.Status.PENDING,
        ).values("receiver")
        return User.objects.filter(id__in=invitation_receiver_ids)


class InvitesReceivedListView(LoginRequiredMixin, ListView):
    template_name = 'friends/invites_received.html'
    context_object_name = 'users'

    def get_queryset(self):
        invitation_sender_ids = FriendInvitation.objects.filter(
            receiver=self.request.user,
            status=FriendInvitation.Status.PENDING,
        ).values("sender")
        return User.objects.filter(id__in=invitation_sender_ids)


class InvitationCreateView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        current_user = self.request.user
        selected_user = get_object_or_404(User, id=user_id)

        # Check for existing invitation
        invitation = FriendInvitation.objects.filter(
            sender=current_user,
            receiver=selected_user,
            status=FriendInvitation.Status.PENDING,
        )

        if not invitation.exists() and current_user != selected_user and not current_user.friendlist.is_friend(selected_user):
            FriendInvitation.objects.create(sender=current_user, receiver=selected_user)

        return HttpResponseRedirect(reverse_lazy('friends:user-search'))


class InvitationAcceptView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        current_user = self.request.user
        selected_user = get_object_or_404(User, id=user_id)

        invitation = FriendInvitation.objects.filter(
            sender=selected_user,
            receiver=current_user,
            status=FriendInvitation.Status.PENDING,
        )

        if invitation.exists():
            # Add users to each others friend lists
            if current_user.friendlist.make_friends(selected_user):
                # Change status to accepted if all went well
                invitation.update(
                    status=FriendInvitation.Status.ACCEPTED,
                )

        return HttpResponseRedirect(reverse_lazy('friends:user-search'))


class InvitationDeclineView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        FriendInvitation.objects.filter(
            sender=get_object_or_404(User, id=user_id),
            receiver=self.request.user,
            status=FriendInvitation.Status.PENDING,
        ).update(
            status=FriendInvitation.Status.DECLINED,
        )

        return HttpResponseRedirect(reverse_lazy('friends:user-search'))


class InvitationCancelView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        FriendInvitation.objects.filter(
            sender=self.request.user,
            receiver=get_object_or_404(User, id=user_id),
            status=FriendInvitation.Status.PENDING,
        ).update(
            status=FriendInvitation.Status.CANCELLED,
        )

        return HttpResponseRedirect(reverse_lazy('friends:user-search'))
