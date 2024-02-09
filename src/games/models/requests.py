from django.db import models, IntegrityError, transaction
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .games import Game


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
                fields=['game'],
                name='unique_pending_request',
                condition=models.Q(status=RequestStatus.PENDING)
            )
        ]

        permissions = [
            ('accept_game_request', 'Can accept game request'),
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
            with transaction.atomic():
                self.game.status = Game.Status.DORMANT
                self.status = self.Status.CANCELLED
                self.game.save()
                self.save()
        except IntegrityError:
            return False
        return True


class GameRequestUser(models.Model):
    """Intermediary M2M Model representing user that requested game to be added"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_request = models.ForeignKey(GameRequest, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=timezone.now)
