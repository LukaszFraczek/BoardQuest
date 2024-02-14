from django.db.models import Subquery, OuterRef
from django.shortcuts import get_object_or_404
from django.contrib import messages
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
        return User.objects.filter(id__in=friends)  # TODO: remove redundant filter!

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
    def post(self, request):
        current_user = self.request.user
        user_to_remove_id = request.POST.get('user_id')
        user_to_remove = get_object_or_404(User, id=user_to_remove_id)

        current_user.friendlist.end_friendship(user_to_remove)

        next_url = request.POST.get('next', 'friends:list')
        return HttpResponseRedirect(next_url)


class InvitationsSentListView(LoginRequiredMixin, ListView):
    template_name = 'friends/invites_sent.html'
    context_object_name = 'users'

    def get_queryset(self):
        # Query invitations sent by current user...
        invitations_sent = FriendInvitation.objects.filter(
            sender=self.request.user,
            status=FriendInvitation.Status.PENDING,
        )

        # Subquery to get invitation id for each user...
        invitations_sent_id = invitations_sent.filter(
            receiver=OuterRef('id')
        ).values('id')[:1]

        # annotate user queryset with invitation_id
        users = User.objects.filter(
            id__in=invitations_sent.values("receiver")
        ).annotate(
            invitation_id=Subquery(invitations_sent_id)
        )

        return users


class InvitationsReceivedListView(LoginRequiredMixin, ListView):
    template_name = 'friends/invites_received.html'
    context_object_name = 'users'

    def get_queryset(self):
        # Query invitations sent TO current user...
        invitations_received = FriendInvitation.objects.filter(
            receiver=self.request.user,
            status=FriendInvitation.Status.PENDING,
        )

        # Subquery to get invitation id for each user...
        invitations_received_id = invitations_received.filter(
            sender=OuterRef('id')
        ).values('id')[:1]

        # annotate user queryset with invitation_id
        users = User.objects.filter(
            id__in=invitations_received.values("sender")
        ).annotate(
            invitation_id=Subquery(invitations_received_id)
        )

        return users


class InvitationsCreateView(LoginRequiredMixin, View):
    def post(self, request):
        user_id = request.POST.get('user_id')
        current_user = self.request.user
        selected_user = get_object_or_404(User, id=user_id)

        # Check for existing invitation
        invitation = FriendInvitation.objects.filter(
            sender=current_user,
            receiver=selected_user,
            status=FriendInvitation.Status.PENDING,
        )

        if invitation.exists():
            messages.warning(request, 'Invitation to this user already exists!')
        elif current_user == selected_user:
            messages.warning(request, 'You cannot invite yourself!')
        elif current_user.friendlist.is_friend(selected_user):
            messages.warning(request, 'This user is already your friend!')
        else:
            FriendInvitation.objects.create(sender=current_user, receiver=selected_user)
            messages.success(request, f'Invite sent to {selected_user.username}!')

        # Extract the "next" parameter from the request
        next_url = request.POST.get('next', 'friends:search')
        return HttpResponseRedirect(next_url)


class InvitationsAcceptView(LoginRequiredMixin, View):
    def post(self, request):
        invitation_id = request.POST.get('invitation_id')
        invitation = get_object_or_404(
            FriendInvitation,
            id=invitation_id,
            status=FriendInvitation.Status.PENDING,
        )

        inv_sender = invitation.sender
        messages.success(request, f'You are now friends with {inv_sender.username}!')

        FriendInvitation.accept(invitation)

        next_url = request.POST.get('next', 'friends:invitations:received')
        return HttpResponseRedirect(next_url)


class InvitationsDeclineView(LoginRequiredMixin, View):
    def post(self, request):
        invitation_id = request.POST.get('invitation_id')
        invitation = get_object_or_404(
            FriendInvitation,
            id=invitation_id,
            status=FriendInvitation.Status.PENDING,
        )

        inv_sender = invitation.sender
        messages.warning(request, f'Invitation from {inv_sender.username} declined')

        FriendInvitation.decline(invitation)

        next_url = request.POST.get('next', 'friends:invitations:received')
        return HttpResponseRedirect(next_url)


class InvitationsCancelView(LoginRequiredMixin, View):
    def post(self, request):
        invitation_id = request.POST.get('invitation_id')
        invitation = get_object_or_404(
            FriendInvitation,
            id=invitation_id,
            status=FriendInvitation.Status.PENDING,
        )

        inv_receiver = invitation.receiver
        messages.warning(request, f'Invitation sent to {inv_receiver.username} cancelled')

        FriendInvitation.cancel(invitation)

        next_url = request.POST.get('next', 'friends:invitations:sent')
        return HttpResponseRedirect(next_url)
