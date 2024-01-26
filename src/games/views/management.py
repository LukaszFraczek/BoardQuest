from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView

from ..models import Game


class RequestedGamesView(LoginRequiredMixin, ListView):
    template_name = 'games/requested_games.html'
    context_object_name = 'games'
    model = Game
    paginate_by = 10

    def get_queryset(self):
        queryset = Game.objects.filter(
                status=Game.Status.REQUESTED,
            )
        return queryset


class AcceptedGamesView(LoginRequiredMixin, ListView):
    template_name = 'games/accepted_games.html'
    context_object_name = 'games'
    model = Game
    paginate_by = 10

    def get_queryset(self):
        queryset = Game.objects.filter(
                status=Game.Status.ACCEPTED,
            )
        return queryset


class UpdateGameView(LoginRequiredMixin, UpdateView):
    model = Game
    template_name = 'games/update.html'
    fields = [
        'primary_name',
        'description',
        'description_short',
        'release_year',
        'players_min',
        'players_max',
        'playtime_min',
        'playtime_max',
        'image_url',
        'thumbnail_url',
    ]

    def get_queryset(self):
        # only accepted games allowed!
        queryset = super().get_queryset()
        queryset = queryset.filter(status=Game.Status.ACCEPTED)
        return queryset