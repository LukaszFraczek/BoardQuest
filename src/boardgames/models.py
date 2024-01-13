from django.db import models
from django.contrib.auth.models import User


class BoardGame(models.Model):
    """Model representing generic boardgame"""

    bgg_id = models.IntegerField(null=False, blank=False)
    name = models.TextField(null=False, blank=False)
    description_short = models.TextField(null=True)
    description = models.TextField(null=True)
    release_date = models.DateTimeField(null=True)
    players_min = models.IntegerField(null=True)
    players_max = models.IntegerField(null=True)
    playtime_min = models.IntegerField(null=True)
    playtime_max = models.IntegerField(null=True)
    image = models.URLField(null=True)
    thumbnail = models.URLField(null=True)
    average_rating = models.FloatField(null=True)

    class Meta:
        unique_together = ('id', 'bgg_id')

    def __str__(self):
        return f"{self.name} board game"


class BoardGameList(models.Model):
    """Model representing a list of owned board games"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    board_games = models.ManyToManyField(User, blank=True, related_name="board_games")

    def __str__(self):
        return f"{self.user} board game list"

    def add(self, board_game):
        if board_game not in self.board_games.all():
            self.board_games.add(board_game)

    def remove(self, board_game):
        if board_game in self.board_games.all():
            self.board_games.remove(board_game)
