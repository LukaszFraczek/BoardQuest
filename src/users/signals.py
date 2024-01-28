from django.db import IntegrityError, transaction
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from icecream import ic

from users.models import Profile
from friends.models import FriendList
from games.models import GameList


@receiver(post_save, sender=User)
def create_new_user_records(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                Profile.objects.create(user=instance)
                FriendList.objects.create(user=instance)
                GameList.objects.create(user=instance)
        except IntegrityError:
            ic("Error while creating new user")
