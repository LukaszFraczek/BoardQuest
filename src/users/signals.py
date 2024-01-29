from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from users.models import Profile
from friends.models import FriendList


@receiver(post_save, sender=User)
def create_new_user_records(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        FriendList.objects.create(user=instance)
