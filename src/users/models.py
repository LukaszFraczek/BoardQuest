from django.contrib.auth.models import User
from django.db import models

from PIL import Image


# max profile image size in px
MAX_IMG_HEIGHT = 300
MAX_IMG_WIDTH = 300


def user_pic_location(instance, filename):
    return f'profile_pics/{instance.user.username}/{filename}'


class Profile(models.Model):
    """Model representing user profile"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField(null=True, blank=True)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to=user_pic_location, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # if profile picture too big, reduce size during save
        img = Image.open(self.image.path)

        if img.height > MAX_IMG_HEIGHT or img.width > MAX_IMG_WIDTH:
            output_size = (MAX_IMG_HEIGHT, MAX_IMG_WIDTH)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f'{self.user.username}\'s profile'
