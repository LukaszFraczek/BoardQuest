from django.db import models, IntegrityError, transaction
from django.contrib.auth.models import User

from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class FriendList(models.Model):
    """Model representing a list of users' friends"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def __str__(self):
        return f"{self.user} friendlist"

    def add(self, user):
        if user not in self.friends.all():
            self.friends.add(user)

    def remove(self, user):
        if user in self.friends.all():
            self.friends.remove(user)

    def end_friendship(self, friend):
        """End friendship between two users. Removes users from each other's friend lists"""

        try:
            with transaction.atomic():
                self.remove(friend)
                friend_flist = FriendList.objects.get(user=friend)
                friend_flist.remove(self.user)
        except IntegrityError:
            # TODO: transaction error handling
            pass

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False


# TODO: implement intermediary model for more info about relation
# class FriendListFriend(models.Model):
#     """Intermediary M2M Model representing user on a friend list and his relation info"""
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     friendlist = models.ForeignKey(FriendList, on_delete=models.CASCADE)
#     since = models.DateTimeField(auto_now_add=timezone.now)


class FriendInvitation(models.Model):
    """Model representing an invitation to friend list"""

    class Status(models.TextChoices):
        ACCEPTED = "Acc", _("Accepted")
        DECLINED = "Dec", _("Declined")
        CANCELLED = "Cld", _("Cancelled")
        PENDING = "Pdg", _("Pending")

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    sent_at = models.DateTimeField(auto_now_add=timezone.now)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.PENDING , null=False, blank=False)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} wants to be friends with {self.receiver}"

    def accept(self):
        """Accept a friend request"""

        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        sender_friend_list = FriendList.objects.get(user=self.sender)

        try:
            receiver_friend_list = FriendList.objects.get(user=self.receiver)
            sender_friend_list = FriendList.objects.get(user=self.sender)
        except:
            # TODO: Error handling
            pass

        receiver_friend_list.add_friend(self.sender)
        sender_friend_list.add_friend(self.receiver)
        self.status = self.Status.ACCEPTED
        self.save()

    def decline(self):
        """Decline a friend request"""
        self.status = self.Status.DECLINED
        self.save()

    def cancel(self):
        """Cancel a friend request"""
        self.status = self.Status.CANCELLED
        self.save()
