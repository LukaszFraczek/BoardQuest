from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


class FriendList(models.Model):
    """Model representing a list of users' friends"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friend_list = models.ManyToManyField(User, blank=True, related_name="friend_list")

    def __str__(self):
        return f"{self.user} friendlist"

    def add(self, user):
        if user not in self.friend_list.all():
            self.friend_list.add(user)

    def remove(self, user):
        if user in self.friend_list.all():
            self.friend_list.remove(user)

    def end_friendship(self, friend):
        """End friendship between two users. Removes users from each other's friend lists"""
        self.remove(friend)
        friend_flist = FriendList.objects.get(user=friend)
        friend_flist.remove(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friend_list.all():
            return True
        return False


# class FriendListFriend(models.Model):
#     """Intermediary M2M Model representing user on a friend list and his relation info"""
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     friendlist = models.ForeignKey(FriendList, on_delete=models.CASCADE)
#     since = models.DateTimeField(auto_now_add=timezone.now)


class FriendInvitation(models.Model):
    """Model representing an invitation to ones friend list"""

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    sent_at = models.DateTimeField(auto_now_add=timezone.now)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} wants to be friends with {self.receiver}"

    def accept(self):
        """Accept a friend request"""
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        sender_friend_list = FriendList.objects.get(user=self.sender)

        if receiver_friend_list:    # TODO: Error handling
            receiver_friend_list.add_friend(self.sender)

        if sender_friend_list:    # TODO: Error handling
            sender_friend_list.add_friend(self.receiver)

    def decline(self):
        """Decline a friend request"""
        self.delete()

    def cancel(self):
        """Cancel a friend request"""
        self.delete()
