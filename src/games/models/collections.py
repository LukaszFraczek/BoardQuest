from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .games import Game


class GameCollection(models.Model):
    """Model representing a collection of owned board games"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="collection")
    games = models.ManyToManyField(Game, through="GameCollectionEntry", blank=True)

    def __str__(self):
        return f"{self.user} game collection"

    def add(self, game: Game):
        if game.status != Game.Status.SUPPORTED:
            return

        if game not in self.games.all():
            self.games.add(game, through_defaults={})

    def remove(self, game: Game):
        if game in self.games.all():
            self.games.remove(game)


class GameCollectionEntry(models.Model):
    """Intermediary M2M Model representing an entry in game collection"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    game_collection = models.ForeignKey(GameCollection, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=timezone.now)
