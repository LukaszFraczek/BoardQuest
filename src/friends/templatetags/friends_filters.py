from django import template
from friends.models import FriendList, FriendInvitation

register = template.Library()


@register.filter
def is_friend(user, friend):
    friend_list = FriendList.objects.get(user=user)
    return friend_list.is_friend(friend)


@register.filter
def invite_pending(user, sender):
    invitation_exists = FriendInvitation.objects.filter(
        receiver=user,
        sender=sender,
        status=FriendInvitation.Status.PENDING,
    ).exists()
    return invitation_exists

