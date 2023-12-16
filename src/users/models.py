from django.db import models
from django.contrib.auth.models import User


def user_pic_location(instance, filename):
    return f'profile_pics/{instance.user.username}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField(null=True)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to=user_pic_location)

    def __str__(self):
        return f'{self.user.username}\'s profile'
