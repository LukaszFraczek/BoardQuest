from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


class Friends(models.Model):
    """Model representing two users being friends"""

    user_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    user_two = models.ForeignKey(User, on_delete=models.CASCADE)
    since = models.DateTimeField(auto_now_add=timezone.now)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"Pair of friends: {self.user_one}, {self.user_two}"


class FriendInvitation(models.Model):
    """Model representing an invitation to ones friendlist"""

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invites_sent")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=timezone.now)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} wants to friends with {self.receiver}"

