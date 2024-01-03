from django.db import IntegrityError, transaction
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
        current_user = self.request.user
        selected_user = get_object_or_404(User, id=user_id)

        # Check for existing invitation
        invitation_exists = FriendInvitation.objects.filter(
            sender=current_user,
            receiver=selected_user,
            status=FriendInvitation.Status.PENDING,
        ).exists()

        if not invitation_exists and current_user != selected_user:
            FriendInvitation.objects.create(sender=current_user, receiver=selected_user)

        return HttpResponseRedirect(reverse_lazy('friends-user-search'))


class InvitationAcceptView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        current_user = self.request.user
        selected_user = get_object_or_404(User, id=user_id)

        invitation_exists = FriendInvitation.objects.get(
            sender=selected_user,
            receiver=current_user,
            status=FriendInvitation.Status.PENDING,
        ).exists()

        if invitation_exists:
            # Add users to each others friend lists
            if current_user.friendlist.make_friends(selected_user):
                # Change status to accepted if all went well
                FriendInvitation.objects.filter(
                    sender=selected_user,
                    receiver=current_user,
                    status=FriendInvitation.Status.PENDING,
                ).update(
                    status=FriendInvitation.Status.ACCEPTED,
                )

        return HttpResponseRedirect(reverse_lazy('friends-user-search'))


class InvitationDeclineView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        current_user = self.request.user
        selected_user = get_object_or_404(User, id=user_id)

        FriendInvitation.objects.filter(
            sender=selected_user,
            receiver=current_user,
            status=FriendInvitation.Status.PENDING,
        ).update(
            status=FriendInvitation.Status.DECLINED,
        )

        return HttpResponseRedirect(reverse_lazy('friends-user-search'))


class InvitationCancelView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        current_user = self.request.user
        selected_user = get_object_or_404(User, id=user_id)

        FriendInvitation.objects.filter(
            sender=current_user,
            receiver=selected_user,
            status=FriendInvitation.Status.PENDING,
        ).update(
            status=FriendInvitation.Status.CANCELLED,
        )

        return HttpResponseRedirect(reverse_lazy('friends-user-search'))
