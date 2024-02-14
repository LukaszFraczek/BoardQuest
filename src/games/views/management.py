from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from ..forms import GameUpdateForm
from ..models import Game


class RequestedGamesView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'games.view_game'
    template_name = 'games/browse/requested.html'
    context_object_name = 'games'
    model = Game
    paginate_by = 10

    def get_queryset(self):
        queryset = Game.objects.filter(
                status=Game.Status.REQUESTED,
            )
        return queryset


class AcceptedGamesView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'games.view_game'
    template_name = 'games/browse/accepted.html'
    context_object_name = 'games'
    model = Game
    paginate_by = 10

    def get_queryset(self):
        queryset = Game.objects.filter(
                status=Game.Status.ACCEPTED,
            )
        return queryset


class UpdateGameView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    ALLOWED_STATUSES = (
        Game.Status.ACCEPTED,
        Game.Status.SUPPORTED,
    )

    permission_required = 'games.change_game'
    template_name = 'games/update.html'
    model = Game
    form_class = GameUpdateForm
    success_url = reverse_lazy('games:accepted_games')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status__in=self.ALLOWED_STATUSES)
        return queryset

    def form_valid(self, form):
        form.instance.status = Game.Status.SUPPORTED
        return super().form_valid(form)
