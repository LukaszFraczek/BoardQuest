from django.db import models
from django.utils.translation import gettext_lazy as _


class Game(models.Model):
    """Model representing generic boardgame"""

    class Status(models.TextChoices):
        REQUESTED = "Req", _("Requested")
        ACCEPTED = "Acc", _("Accepted")
        SUPPORTED = "Sup", _("Supported")
        REJECTED = "Rej", _("Rejected")
        DORMANT = "Dor", _("Dormant")

    status = models.CharField(max_length=3, choices=Status.choices, default=Status.REQUESTED, null=False, blank=False)
    bgg_id = models.IntegerField(null=False, blank=False)
    primary_name = models.TextField(null=False, blank=False)
    description = models.TextField(null=True)
    description_short = models.TextField(null=True, blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    players_min = models.IntegerField(null=True)
    players_max = models.IntegerField(null=True)
    playtime_min = models.IntegerField(null=True)
    playtime_max = models.IntegerField(null=True)
    image_url = models.URLField(null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)

    class Meta:
        unique_together = ('id', 'bgg_id')

    def __str__(self):
        return f"{self.primary_name} board game"
