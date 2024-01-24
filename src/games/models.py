from django.db import models, IntegrityError, transaction
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Game(models.Model):
    """Model representing generic boardgame"""

    class Status(models.TextChoices):
        REQUESTED = "Req", _("Requested")
        ACCEPTED = "Acc", _("Accepted")
        SUPPORTED = "Sup", _("Supported")
        REJECTED = "Rej", _("Rejected")

    status = models.CharField(max_length=3, choices=Status.choices, default=Status.REQUESTED, null=False, blank=False)
    bgg_id = models.IntegerField(null=False, blank=False)
    primary_name = models.TextField(null=False, blank=False)
    description = models.TextField(null=True)
    description_short = models.TextField(null=True)
    release_year = models.DateField(null=True)
    players_min = models.IntegerField(null=True)
    players_max = models.IntegerField(null=True)
    playtime_min = models.IntegerField(null=True)
    playtime_max = models.IntegerField(null=True)
    image_url = models.URLField(null=True)
    thumbnail_url = models.URLField(null=True)
    # average_rating = models.FloatField(null=True)

    class Meta:
        unique_together = ('id', 'bgg_id')

    def __str__(self):
        return f"{self.primary_name} board game"


class GameList(models.Model):
    """Model representing a list of owned board games"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game, through="BoardGameListEntry", blank=True, related_name="board_games")

    def __str__(self):
        return f"{self.user} board game list"

    def add(self, board_game: Game):
        if board_game.Status != Game.Status.SUPPORTED:
            return

        if board_game not in self.games.all():
            self.games.add(board_game, through_defaults={})

    def remove(self, board_game: Game):
        if board_game in self.games.all():
            self.games.remove(board_game)


class BoardGameListEntry(models.Model):
    """Intermediary M2M Model representing an entry in board game list"""

    board_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    board_game_list = models.ForeignKey(GameList, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=timezone.now)


class RequestStatus(models.TextChoices):
    ACCEPTED = "Acc", _("Accepted")
    DECLINED = "Dec", _("Declined")
    CANCELLED = "Cld", _("Cancelled")
    PENDING = "Pdg", _("Pending")


class GameRequest(models.Model):
    """Model representing a request to add a boardgame to library of supported games"""

    Status = RequestStatus

    status = models.CharField(max_length=3, choices=Status.choices, default=Status.PENDING, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="request")
    users = models.ManyToManyField(User, through="GameRequestUser")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['board_game'],
                name='unique_pending_request',
                condition=models.Q(status=RequestStatus.PENDING)
            )
        ]

    def __str__(self):
        return f"Request to add {self.game}"

    def accept(self) -> bool:
        """Accept request to add a game to game library"""

        try:
            with transaction.atomic():
                self.game.status = Game.Status.ACCEPTED
                self.status = self.Status.ACCEPTED
                self.game.save()
                self.save()
        except IntegrityError:
            return False
        return True

    def decline(self) -> bool:
        """Decline request to add a game to game library"""

        try:
            with transaction.atomic():
                self.game.status = Game.Status.REJECTED
                self.status = self.Status.DECLINED
                self.game.save()
                self.save()
        except IntegrityError:
            return False
        return True

    def cancel(self) -> bool:
        """Cancel request to add a game to game library"""

        try:
            self.status = self.Status.CANCELLED
            self.save()
        except IntegrityError:
            return False
        return True


class GameRequestUser(models.Model):
    """Intermediary M2M Model representing user that requested game to be added"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_request = models.ForeignKey(GameRequest, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=timezone.now)
