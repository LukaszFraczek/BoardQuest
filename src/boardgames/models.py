from django.db import models


class BoardGame(models.Model):
    """Model representing generic boardgame"""

    bgg_id = models.IntegerField(null=False, blank=False)
    name = models.TextField(null=False, blank=False)
    description = models.TextField(null=True)
    release_date = models.DateTimeField(null=True)
    players_min = models.IntegerField(null=True)
    players_max = models.IntegerField(null=True)
    image = models.URLField(null=True)
    thumbnail = models.URLField(null=True)
    average_rating = models.FloatField(null=True)

    class Meta:
        unique_together = ('id', 'bgg_id')
